using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Application.Interfaces;
using Microsoft.EntityFrameworkCore.Storage;

namespace BlogPlatform.Infrastructure.Persistance
{
    public class UnitOfWork : IUnitOfWork
    {
        private readonly AppDbContext _context;
        private IDbContextTransaction? _transaction;
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

        public async Task BeginTransactionAsync()
        {
            _transaction = await _context.Database.BeginTransactionAsync();
        }

        public async Task CommitTransactionAsync()
        {
            await _context.SaveChangesAsync();
            if (_transaction != null)
            {
                await _transaction!.CommitAsync();
            }
        }

        public async Task RollbackTransactionAsync()
        {
            if (_transaction != null)
                await _transaction!.RollbackAsync();
        }
    }
}