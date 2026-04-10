using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Application.DTOs.Blog;
using BlogPlatform.Application.Interfaces;
using BlogPlatform.Domain.Entities;

namespace BlogPlatform.Application.Services
{
    public class BlogService : IBlogService
    {
        private readonly IUnitOfWork _unitOfWork;

        public BlogService(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }
        public async Task<BlogDto> CreateBlog(CreateBlogDto dto, Guid userId)
        {
            var blog = new Blog
            {
                Content = dto.Content,
                Id = Guid.NewGuid(),
                Title = dto.Title,
                UserId = userId
            };

            await _unitOfWork.Blog.AddAsync(blog);
            return new BlogDto
            {
                Id = blog.Id,
                Title = blog.Title,
                Content = blog.Content,
            };

        }

        public async Task<BlogDto> CreateBlogWithCommentAsync(CreateBlogWithCommentDto dto, Guid userId)
        {
            await _unitOfWork.BeginTransactionAsync();
            try
            {
                var blog = new Blog
                {
                    Id = Guid.NewGuid(),
                    Title = dto.Title,
                    Content = dto.Content,
                    UserId = userId
                };
                await _unitOfWork.Blog.AddAsync(blog);
                var comment = new Comment
                {
                    Id = Guid.NewGuid(),
                    Content = dto.InitialComment,
                    BlogId = blog.Id,
                    UserId = userId,
                    CreatedDate = DateTime.UtcNow
                };
                await _unitOfWork.Comment.AddAsync(comment);
                await _unitOfWork.CommitTransactionAsync();
                return new BlogDto
                {
                    Id = blog.Id,
                    Title = blog.Title,
                    Content = blog.Content,
                };
            }
            catch
            {
                await _unitOfWork.RollbackTransactionAsync();
                throw;
            }
        }

        public async Task<bool> DeleteBlogAsync(Guid id, Guid userId)
        {
            var blog = await _unitOfWork.Blog.GetByIdAsync(id);
            if (blog == null)
            {
                return false;
            }
            if (blog.UserId != userId)
            {
                throw new UnauthorizedAccessException("You cannot delete this blog");
            }
            await _unitOfWork.Blog.DeleteAsync(blog);
            return true;
        }

        public async Task<List<BlogDto>> GetAllBlogsAsync(int page, int pageSize, Guid userId)
        {
            var blogs = await _unitOfWork.Blog.GetAllAsync(page, pageSize, userId);
            var result = new List<BlogDto>();
            return [.. blogs.Select(b => new BlogDto
            {
                Id = b.Id,
                Title = b.Title,
                Content = b.Content,
                CreatedAt = b.CreatedDate,
            })];

        }

        public async Task<BlogDto?> GetBlogByIdAsync(Guid id)
        {
            var blog = await _unitOfWork.Blog.GetByIdAsync(id);
            if (blog == null)
            {
                return null;
            }
            return new BlogDto
            {
                Id = blog.Id,
                Title = blog.Title,
                Content = blog.Content,
                CreatedAt = blog.CreatedDate,
            };
        }

        public async Task<bool> UpdateBlogAsync(Guid id, UpdateBlogDto dto, Guid userId)
        {
            var blog = await _unitOfWork.Blog.GetByIdAsync(id);
            if (blog == null) return false;

            if (blog.UserId != userId)
                throw new UnauthorizedAccessException("You cannot edit this blog");

            blog.Title = dto.Title;
            blog.Content = dto.Content;
            await _unitOfWork.Blog.UpdateAsync(blog);
            return true;
        }
    }
}