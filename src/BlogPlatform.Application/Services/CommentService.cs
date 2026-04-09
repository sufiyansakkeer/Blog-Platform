using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Application.DTOs.Comment;
using BlogPlatform.Application.Interfaces;
using BlogPlatform.Domain.Entities;

namespace BlogPlatform.Application.Services
{
    public class CommentService : ICommentService
    {
        private readonly IUnitOfWork _unitOfWork;



        public CommentService(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }
        public async Task<CommentResponseDto> CreateComment(CreateCommentDto dto, Guid userId, Guid blogId)
        {
            var blog = await _unitOfWork.Blog.GetByIdAsync(blogId);
            if (blog == null)
            {
                throw new KeyNotFoundException($"Blog page {blogId} not found");
            }
            if (dto.ParentCommentId.HasValue)
            {
                var parent = await _unitOfWork.Comment.GetByIdAsync(dto.ParentCommentId.Value);
                if (parent == null || parent.BlogId != blogId)
                {
                    throw new ArgumentException("Invalid parent comment");
                }
            }


            var comment = new Comment
            {
                Id = Guid.NewGuid(),
                Content = dto.Content,
                BlogId = blogId,
                UserId = userId,
                CreatedDate = DateTime.UtcNow,
                ParentCommentId = dto.ParentCommentId,

            };
            await _unitOfWork.Comment.AddAsync(comment);
            await _unitOfWork.SaveChangesAsync();
            return new CommentResponseDto
            {
                Id = comment.Id,
                Content = comment.Content,
                BlogId = comment.BlogId,
                UserId = comment.UserId,
                CreatedAt = comment.CreatedDate,


            };
        }

        public async Task<List<CommentResponseDto>> GetCommentByBlogAsync(Guid blogId, int page, int pageSize)
        {

            // Step 1: Top-level comments
            var parents = await _unitOfWork.Comment.GetTopLevelComments(blogId, page, pageSize);

            var parentIds = parents.Select(p => p.Id).ToList();

            // Step 2: Get ALL nested replies
            var replies = await _unitOfWork.Comment.GetRepliesByParentIds(parentIds);

            // Step 3: Combine
            var allComments = parents.Concat(replies)
                .OrderByDescending(c => c.CreatedDate)
                .ToList();

            // Step 4: Build tree
            return BuildCommentTree(allComments);



        }


        public async Task<bool> DeleteComment(Guid commentId, Guid userId)
        {
            var comment = await _unitOfWork.Comment.GetByIdAsync(commentId);
            if (comment == null)
            {
                return false;
            }
            if (comment.UserId != userId)
            {
                throw new UnauthorizedAccessException("You can't delete this comment");
            }
            comment.IsDeleted = true;
            comment.DeletedAt = DateTime.UtcNow;
            _unitOfWork.Comment.Update(comment);
            await _unitOfWork.SaveChangesAsync();
            return true;

        }

        private static List<CommentResponseDto> BuildCommentTree(List<Comment> comments)
        {
            var lookup = comments.ToLookup(c => c.ParentCommentId);
            List<CommentResponseDto> Build(Guid? parentId)
            {
                return lookup[parentId]
                  .Select(c => new CommentResponseDto
                  {
                      Id = c.Id,
                      Content = c.Content,
                      BlogId = c.BlogId,
                      UserId = c.UserId,
                      CreatedAt = c.CreatedDate,
                      Replies = Build(c.Id)

                  }).ToList();

            }
            ;
            return Build(null);
        }

    }
}