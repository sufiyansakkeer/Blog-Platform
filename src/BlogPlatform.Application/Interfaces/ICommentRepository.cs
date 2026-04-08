using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Domain.Entities;

namespace BlogPlatform.Application.Interfaces
{
    public interface ICommentRepository
    {
        Task<Comment?> GetByIdAsync(Guid id);
        Task AddAsync(Comment comment);
        Task<List<Comment>> GetByBlogIdAsync(Guid blogId, int page, int pageSize);
        Task DeleteAsync(Comment comment);
        Task<List<Comment>> GetTopLevelComments(Guid blogId, int page, int pageSize);
        Task<List<Comment>> GetRepliesByParentIds(List<Guid> parentIds);

    }
}