using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Application.DTOs.Blog;

namespace BlogPlatform.Application.Services
{
    public interface IBlogService
    {
        Task<BlogDto> CreateBlog(CreateBlogDto dto, Guid userId);
        Task<List<BlogDto>> GetAllBlogsAsync(int page, int pageSize, Guid userId);

        Task<BlogDto?> GetBlogByIdAsync(Guid id);

        Task<bool> UpdateBlogAsync(Guid id, UpdateBlogDto dto, Guid userId);

        Task<bool> DeleteBlogAsync(Guid id, Guid userId);
        Task<BlogDto> CreateBlogWithCommentAsync(CreateBlogWithCommentDto dto, Guid userId);

    }
}