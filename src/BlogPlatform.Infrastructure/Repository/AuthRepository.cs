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
    public class AuthRepository : IAuthRepository
    {
        private readonly AppDbContext _context;

        public AuthRepository(AppDbContext context)
        {
            _context = context;
        }
        public async Task AddAsync(User user)
        {
            await _context.Users.AddAsync(user);
            await _context.SaveChangesAsync();

        }

        public async Task<User?> GetByEmailAsync(string Email)
        {
            return await _context.Users.FirstOrDefaultAsync(x => x.Email == Email);
        }
    }
}