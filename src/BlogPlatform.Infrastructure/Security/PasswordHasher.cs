using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Application.Interfaces;

namespace BlogPlatform.Infrastructure.Security
{
    public class PasswordHasher : IPasswordHasher
    {
        public string Hash(string Password)
        {
            return BCrypt.Net.BCrypt.HashPassword(Password);
        }

        public bool Verify(string Password, string HashedPassword)
        {
            return BCrypt.Net.BCrypt.Verify(Password, HashedPassword);
        }
    }
}