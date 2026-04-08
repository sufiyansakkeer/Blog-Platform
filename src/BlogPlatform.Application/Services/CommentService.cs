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
        private readonly ICommentRepository _commentRepository;
        private readonly IBlogRepository _blogRepository;



        public CommentService(ICommentRepository commentRepository, IBlogRepository blogRepository)
        {
            _commentRepository = commentRepository;
            _blogRepository = blogRepository;
        }
        public async Task<CommentResponseDto> CreateComment(CreateCommentDto dto, Guid userId, Guid blogId)
        {
            var blog = await _blogRepository.GetByIdAsync(blogId);
            if (blog == null)
            {
                throw new KeyNotFoundException($"Blog page {blogId} not found");
            }
            if (dto.ParentCommentId.HasValue)
            {
                var parent = await _commentRepository.GetByIdAsync(dto.ParentCommentId.Value);
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
            await _commentRepository.AddAsync(comment);
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
            var blog = await _blogRepository.GetByIdAsync(blogId);
            if (blog == null)
                throw new KeyNotFoundException("Blog not found");

            // Step 1: Top-level comments
            var parents = await _commentRepository.GetTopLevelComments(blogId, page, pageSize);

            var parentIds = parents.Select(p => p.Id).ToList();

            // Step 2: Get ALL nested replies
            var replies = await _commentRepository.GetRepliesByParentIds(parentIds);

            // Step 3: Combine
            var allComments = parents.Concat(replies)
                .OrderByDescending(c => c.CreatedDate)
                .ToList();

            // Step 4: Build tree
            return BuildCommentTree(allComments);



        }


        public async Task<bool> DeleteComment(Guid commentId, Guid userId)
        {
            var comment = await _commentRepository.GetByIdAsync(commentId);
            if (comment == null)
            {
                return false;
            }
            if (comment.UserId != userId)
            {
                throw new ArgumentException("You can't delete this comment");
            }
            await _commentRepository.DeleteAsync(comment);
            return true;

        }
        private static CommentResponseDto MapToDto(Comment comment) => new()
        {
            Id = comment.Id,
            Content = comment.Content,
            BlogId = comment.BlogId,
            UserId = comment.UserId,
            CreatedAt = comment.CreatedDate,
        };

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