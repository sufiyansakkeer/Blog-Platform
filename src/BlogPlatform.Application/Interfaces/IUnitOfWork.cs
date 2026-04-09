using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BlogPlatform.Application.Interfaces
{
    public interface IUnitOfWork
    {
        ICommentRepository Comment { get; }
        IBlogRepository Blog { get; }

        Task<int> SaveChangesAsync();
    }
}