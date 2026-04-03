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
    public class BlogRepository : IBlogRepository
    {
        private readonly AppDbContext _context;
        public BlogRepository(AppDbContext context)
        {
            _context = context;
        }



        public async Task AddAsync(Blog blog)
        {
            _context.Blogs.Add(blog);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteAsync(Blog blog)
        {
            _context.Blogs.Remove(blog);
            await _context.SaveChangesAsync();
        }

        public async Task<List<Blog>> GetAllAsync(int page, int pageSize, Guid userId)
        {
            page = page < 1 ? 1 : page;
            return await _context.Blogs
            .AsNoTracking()
            .Where(x => x.UserId == userId)
            .OrderByDescending(x => x.CreatedDate)
            .Skip((page - 1) * pageSize).Take(pageSize)
            .ToListAsync();

        }

        public async Task<Blog?> GetByIdAsync(Guid id)
        {
            return await _context.Blogs.FirstOrDefaultAsync(x => x.Id == id);
        }

        public async Task UpdateAsync(Blog blog)
        {
            _context.Blogs.Update(blog);
            await _context.SaveChangesAsync();

        }
    }
}