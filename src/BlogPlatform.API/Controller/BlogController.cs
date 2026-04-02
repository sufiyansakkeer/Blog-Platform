using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using BlogPlatform.Application.Common;
using BlogPlatform.Application.DTOs.Blog;
using BlogPlatform.Application.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace BlogPlatform.API.Controller
{
    [Authorize]
    [ApiController]
    [Route("api/blog")]
    public class BlogController : ControllerBase
    {

        private readonly IBlogService _blog;

        public BlogController(IBlogService blog)
        {
            _blog = blog;
        }

        [HttpGet]

        public async Task<IActionResult> GetAll()
        {
            var blogs = await _blog.GetAllBlogsAsync();


            return Ok(new ApiResponse<List<BlogDto>>
            {
                Success = true,
                Message = "All blogs retrieved successfully",
                Data = blogs,
            });

        }

        [HttpPost]
        public async Task<IActionResult> Create(CreateBlogDto dto)
        {
            var userId = GetUserId();
            await _blog.CreateBlog(dto, userId);

            return Ok(new ApiResponse<string?>
            {
                Success = true,
                Message = "Blog created successfully"
            });
        }
        [HttpGet("{id}")]
        public async Task<IActionResult> GetById(Guid id)
        {
            var blog = await _blog.GetBlogByIdAsync(id);
            if (blog == null)
            {
                return NotFound(new ApiResponse<string?>
                {
                    Success = false,
                    Message = "Blog not found"

                });
            }
            return Ok(new ApiResponse<BlogDto>
            {
                Data = blog,
                Success = true,
                Message = "Blog retrieved successfully"
            });
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, UpdateBlogDto dto)
        {
            var userId = GetUserId();
            var result = await _blog.UpdateBlogAsync(id, dto, userId);
            if (!result) return NotFound(
                new ApiResponse<string?>
                {
                    Success = false,
                    Message = "Blog not found"
                }
            );

            return Ok(new ApiResponse<string?>
            {
                Success = true,
                Message = "Blog updated successfully"
            });

        }
        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(Guid id)
        {
            var userId = GetUserId();
            var result = await _blog.DeleteBlogAsync(id, userId);
            if (!result) return NotFound(
                new ApiResponse<string?>
                {
                    Success = false,
                    Message = "Blog not found"
                }
            );

            return NoContent(

            );

        }

        private Guid GetUserId()
        {
            var userIdClaim = User.FindFirst("id")?.Value ??
                             User.FindFirst(ClaimTypes.NameIdentifier)?.Value ??
                             throw new UnauthorizedAccessException("User ID claim not found.");

            if (!Guid.TryParse(userIdClaim, out var userId))
                throw new UnauthorizedAccessException("Invalid user ID format.");

            return userId;
        }
    }
}