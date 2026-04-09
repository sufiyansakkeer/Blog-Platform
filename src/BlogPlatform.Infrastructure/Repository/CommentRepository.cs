using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Application.Interfaces;
using BlogPlatform.Domain.Entities;
using BlogPlatform.Infrastructure.Persistance;
using Microsoft.EntityFrameworkCore;

namespace BlogPlatform.Infrastructure.Repository
{
    public class CommentRepository : ICommentRepository
    {
        private readonly AppDbContext _context;

        public CommentRepository(AppDbContext context)
        {
            _context = context;
        }
        public async Task AddAsync(Comment comment)
        {
            await _context.Comments.AddAsync(comment);
        }

        public void Delete(Comment comment)
        {

            _context.Comments.Remove(comment);

        }
        public void Update(Comment comment)
        {
            _context.Comments.Update(comment);
        }

        public async Task<List<Comment>> GetByBlogIdAsync(Guid blogId, int page, int pageSize)
        {
            page = page < 1 ? 1 : page;
            pageSize = pageSize < 1 ? 1 : pageSize;
            return await _context.Comments
            .Where(c => c.BlogId == blogId)
            .OrderByDescending(c => c.CreatedDate)
            .Skip((page - 1) * pageSize)
            .Take(pageSize).ToListAsync();
        }

        public async Task<Comment?> GetByIdAsync(Guid id)
        {
            return await _context.Comments.FirstOrDefaultAsync(c => c.Id == id);
        }
        public async Task<List<Comment>> GetTopLevelComments(Guid blogId, int page, int pageSize)
        {
            page = page < 1 ? 1 : page;
            pageSize = pageSize < 1 ? 1 : pageSize;
            return await _context.Comments
                .Where(c => c.BlogId == blogId && c.ParentCommentId == null)
                .OrderByDescending(c => c.CreatedDate)
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();
        }
        public async Task<List<Comment>> GetRepliesByParentIds(List<Guid> parentIds)
        {
            return await _context.Comments
                .Where(c => c.ParentCommentId != null && parentIds.Contains(c.ParentCommentId.Value))
                .OrderByDescending(c => c.CreatedDate)
                .ToListAsync();
        }
    }
}