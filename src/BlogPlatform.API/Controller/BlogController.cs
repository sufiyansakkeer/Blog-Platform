using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
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
            return Ok(await _blog.GetAllBlogsAsync());

        }

        [HttpPost]
        public async Task<IActionResult> Create(CreateBlogDto dto)
        {
            var userId = GetUserId();
            await _blog.CreateBlog(dto, userId);

            return Ok("Blog created");
        }
        [HttpGet("{id}")]
        public async Task<IActionResult> GetById(Guid id)
        {
            var blog = await _blog.GetBlogByIdAsync(id);
            if (blog == null)
            {
                return NotFound();
            }
            return Ok(blog);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(Guid id, UpdateBlogDto dto)
        {
            var userId = GetUserId();
            var result = await _blog.UpdateBlogAsync(id, dto, userId);
            if (!result) return NotFound();

            return Ok("Updated successfully");

        }
        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(Guid id)
        {
            var userId = GetUserId();
            var result = await _blog.DeleteBlogAsync(id, userId);
            if (!result) return NotFound();

            return NoContent();

        }

        private Guid GetUserId()
        {
            var userId = Guid.Parse(ClaimTypes.NameIdentifier ?? User.FindFirst("id")?.Value ?? throw new UnauthorizedAccessException("User ID claim not found."));
            return userId;
        }
    }
}