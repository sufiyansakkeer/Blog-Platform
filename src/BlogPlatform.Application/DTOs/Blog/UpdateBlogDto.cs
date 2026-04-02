using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BlogPlatform.Application.DTOs.Blog
{
    public class UpdateBlogDto
    {
        public string Title { get; set; }
        public string Content { get; set; }
    }
}