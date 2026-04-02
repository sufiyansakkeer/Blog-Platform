using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BlogPlatform.Application.Interfaces
{
    public interface IPasswordHasher
    {
        string Hash(string Password);
        bool Verify(string Password, string HashedPassword);

    }
}