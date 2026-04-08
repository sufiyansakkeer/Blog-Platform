using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Application.DTOs.Comment;

namespace BlogPlatform.Application.Services
{
    public interface ICommentService
    {
        Task<List<CommentResponseDto>> GetCommentByBlogAsync(Guid blogId, int page, int pageSize);
        Task<CommentResponseDto> CreateComment(CreateCommentDto dto, Guid userId, Guid blogId);
        Task<bool> DeleteComment(Guid commentId, Guid userId);
    }
}