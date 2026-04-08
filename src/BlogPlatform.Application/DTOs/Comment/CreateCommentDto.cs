using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BlogPlatform.Application.DTOs.Comment
{
    public class CreateCommentDto
    {
        public string Content { get; set; } = null!;
        public Guid BlogId { get; set; }
        public Guid? ParentCommentId { get; set; }
    }
}