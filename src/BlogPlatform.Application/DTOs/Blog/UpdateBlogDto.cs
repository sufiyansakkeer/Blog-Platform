using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Application.DTOs.Comment;

namespace BlogPlatform.Application.DTOs.Blog
{
    public class UpdateBlogDto
    {
        public string Title { get; set; } = null!;
        public string Content { get; set; } = null!;

    }
}