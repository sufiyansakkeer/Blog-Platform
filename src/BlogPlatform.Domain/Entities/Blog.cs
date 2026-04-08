using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BlogPlatform.Domain.Entities
{
    public class Blog
    {
        public Guid Id { get; set; }
        public string Title { get; set; } = null!;
        public string Content { get; set; } = null!;
        public DateTime CreatedDate { get; set; } = DateTime.UtcNow;

        public Guid UserId { get; set; }
        public ICollection<Comment> Comments { get; set; } = [];
    }
}