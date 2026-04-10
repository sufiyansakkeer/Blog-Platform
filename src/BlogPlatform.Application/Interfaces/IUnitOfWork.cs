using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore.Storage;

namespace BlogPlatform.Application.Interfaces
{
    public interface IUnitOfWork
    {
        ICommentRepository Comment { get; }
        IBlogRepository Blog { get; }

        Task<int> SaveChangesAsync();
        Task BeginTransactionAsync();
        Task CommitTransactionAsync();
        Task RollbackTransactionAsync();
    }
}