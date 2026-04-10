using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BlogPlatform.Application.DTOs.Blog
{
    public class CreateBlogWithCommentDto
    {
        public string Title { get; set; } = string.Empty;
        public string Content { get; set; } = string.Empty;
        public string InitialComment { get; set; } = string.Empty;
    }
}