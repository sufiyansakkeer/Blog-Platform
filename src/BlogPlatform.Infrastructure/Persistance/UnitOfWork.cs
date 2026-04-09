using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Application.Interfaces;

namespace BlogPlatform.Infrastructure.Persistance
{
    public class UnitOfWork : IUnitOfWork
    {
        private readonly AppDbContext _context;
        public ICommentRepository Comment { get; }


        public IBlogRepository Blog { get; }

        public UnitOfWork(ICommentRepository commentRepository, IBlogRepository blogRepository, AppDbContext context)
        {
            Comment = commentRepository;
            Blog = blogRepository;
            _context = context;
        }

        public async Task<int> SaveChangesAsync()
        {
            return await _context.SaveChangesAsync();
        }
    }
}