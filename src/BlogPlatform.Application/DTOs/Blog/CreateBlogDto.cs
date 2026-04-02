using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace BlogPlatform.Application.DTOs.Blog
{
    public class CreateBlogDto
    {
        [Required]
        [MaxLength(150)]
        public string Title { get; set; }
        [Required]
        public string Content { get; set; }
    }
}