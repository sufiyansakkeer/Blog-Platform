using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using BlogPlatform.Application.Common;
using BlogPlatform.Application.DTOs.Comment;
using BlogPlatform.Application.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace BlogPlatform.API.Controller
{
    [ApiController]
    [Route("api/blog/{blogId}/comments")]
    public class CommentController : ControllerBase
    {
        private readonly ICommentService _commentService;

        public CommentController(ICommentService commentService)
        {
            _commentService = commentService;

        }

        [Authorize]
        [HttpPost]
        public async Task<IActionResult> CreateComment(Guid blogId, [FromBody] CreateCommentDto dto)
        {
            var userId = GetUserId();
            var result = await _commentService.CreateComment(dto, userId, blogId);
            return CreatedAtAction(nameof(CreateComment), new ApiResponse<CommentResponseDto>
            {
                Success = true,
                Message = "Comment created successfully",
                Data = result
            });
        }

        [HttpGet]
        public async Task<IActionResult> GetCommnet(Guid blogId, [FromQuery] int page, [FromQuery] int pageSize)
        {
            if (page <= 0 || pageSize <= 0)
            {
                return BadRequest("Invalid pagination Values");
            }
            pageSize = Math.Min(pageSize, 50);
            var result = await _commentService.GetCommentByBlogAsync(blogId, page, pageSize);
            return Ok(new ApiResponse<List<CommentResponseDto>>
            {
                Success = true,
                Message = "Comments retrieved successfully",
                Data = result
            });

        }
        [Authorize]
        [HttpDelete("{commentId}")]
        public async Task<IActionResult> DeleteComment(Guid blogId, Guid commentId)
        {
            var userId = GetUserId();
            var result = await _commentService.DeleteComment(commentId, userId);
            if (!result)
            {
                return NotFound();
            }
            return NoContent();
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