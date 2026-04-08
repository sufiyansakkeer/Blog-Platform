using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BlogPlatform.Application.DTOs.Comment
{
    public class CommentResponseDto
    {
        public Guid Id { get; set; }
        public string Content { get; set; }
        public Guid BlogId { get; set; }
        public Guid UserId { get; set; }
        public DateTime CreatedAt { get; set; }
        public List<CommentResponseDto> Replies { get; set; } = [];

    }
}