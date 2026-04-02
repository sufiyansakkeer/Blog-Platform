using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Domain.Entities;

namespace BlogPlatform.Application.Interfaces
{
    public interface IJwtGenerator
    {
        string GenerateToken(User user);
    }
}