using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Application.DTOs.Auth;
using BlogPlatform.Application.Interfaces;
using BlogPlatform.Domain.Entities;

namespace BlogPlatform.Application.Services
{
    public class AuthService : IAuthService
    {
        private readonly IAuthRepository _authRepo;
        private readonly IPasswordHasher _hasher;
        private readonly IJwtGenerator _jwt;

        public AuthService(IAuthRepository authRepo, IPasswordHasher hasher, IJwtGenerator jwt)
        {
            _authRepo = authRepo;
            _hasher = hasher;
            _jwt = jwt;
        }
        public async Task<AuthResponseDto> LoginAsync(LoginDto request)
        {
            var user = await _authRepo.GetByEmailAsync(request.Email) ?? throw new Exception("Email or Password is incorrect");
            if (!_hasher.Verify(request.Password, user.PasswordHash))
                throw new Exception("Email or Password is incorrect");

            var token = _jwt.GenerateToken(user);

            return new AuthResponseDto
            {
                Token = token
            };



        }

        public async Task<AuthResponseDto> RegisterAsync(RegisterDto request)
        {
            var user = await _authRepo.GetByEmailAsync(request.Email);
            if (user != null) throw new Exception("User already exist");

            var hashPassword = _hasher.Hash(request.Password);
            var newUser = new User
            {
                Email = request.Email,
                PasswordHash = hashPassword,
                Id = Guid.NewGuid(),

            };

            var token = _jwt.GenerateToken(newUser);
            await _authRepo.AddAsync(newUser);

            return new AuthResponseDto
            {
                Token = token
            };
        }
    }
}