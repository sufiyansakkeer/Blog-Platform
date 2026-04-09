using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace BlogPlatform.Infrastructure.Persistance
{
    public class AppDbContext : DbContext
    {
        public DbSet<User> Users { get; set; }
        public DbSet<Blog> Blogs { get; set; }

        public DbSet<Comment> Comments { get; set; }

        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {

        }
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<Blog>()
                .Property(b => b.CreatedDate)
                .HasDefaultValueSql("GETUTCDATE()");
            // Blog -> comments
            modelBuilder.Entity<Comment>()
                .HasOne(c => c.Blog)
                .WithMany(b => b.Comments)
                .HasForeignKey(c => c.BlogId)
                .OnDelete(DeleteBehavior.Cascade);

            modelBuilder.Entity<Comment>()
            .Property(b => b.CreatedDate)
            .HasDefaultValueSql("GETUTCDATE()");

            modelBuilder.Entity<Comment>()
            .HasQueryFilter(c => !c.IsDeleted);

            // Comment -> parent comment
            modelBuilder.Entity<Comment>()
                .HasOne(c => c.ParentComment)
                .WithMany(c => c.Replies)
                .HasForeignKey(c => c.ParentCommentId)
                .OnDelete(DeleteBehavior.NoAction); // safer

            // Index
            modelBuilder.Entity<Comment>()
                .HasIndex(c => new { c.BlogId, c.ParentCommentId });
        }
    }
}