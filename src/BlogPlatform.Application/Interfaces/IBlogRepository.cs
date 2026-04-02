using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Domain.Entities;

namespace BlogPlatform.Application.Interfaces
{
    public interface IBlogRepository
    {
        Task AddAsync(Blog blog);
        Task<List<Blog>> GetAllAsync();
        Task<Blog?> GetByIdAsync(Guid id);
        Task UpdateAsync(Blog blog);
        Task DeleteAsync(Blog blog);
    }
}