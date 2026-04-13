using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using BlogPlatform.Application.Common;
using BlogPlatform.Application.DTOs.Blog;
using BlogPlatform.IntegrationTests.Base;
using BlogPlatform.IntegrationTests.Factories;
using FluentAssertions;
using Xunit;

namespace BlogPlatform.IntegrationTests.Tests
{
    public class BlogTests : TestBase
    {
        public BlogTests(CustomWebApplicationFactory factory)
        : base(factory)
        { }
        [Fact]
        public async Task CreateBlog_ShouldReturnSuccess()
        {
            var blog = new
            {
                title = "Test Blog",
                content = "Test Content"
            };
            var content = new StringContent(
                JsonSerializer.Serialize(blog),
                Encoding.UTF8,
                "application/json"
            );

            var response = await _client.PostAsync("/api/blog", content);
            var body = await response.Content.ReadAsStringAsync();
            Console.WriteLine(body);
            response.StatusCode.Should().BeOneOf(HttpStatusCode.OK, HttpStatusCode.Created);
        }
        [Fact]
        public async Task DeleteBlog_ShouldSoftDelete()
        {
            // Given
            var blog = new { title = "Temp", content = "Temp" };
            var createResponse = await _client.PostAsJsonAsync("/api/blog", blog);
            createResponse.EnsureSuccessStatusCode();
            
            // Create a blog and get its ID by creating it directly through the service
            var getAllResponse = await _client.GetAsync("/api/blog?page=1&pageSize=1");
            getAllResponse.EnsureSuccessStatusCode();
            var getAllResult = await getAllResponse.Content.ReadFromJsonAsync<ApiResponse<List<BlogDto>>>();
            getAllResult.Data.Should().NotBeNull();
            var created = getAllResult.Data.FirstOrDefault();
            created.Should().NotBeNull();

            // When
            var deleteResponse = await _client.DeleteAsync($"/api/blog/{created.Id}");
            deleteResponse.StatusCode.Should().Be(HttpStatusCode.NoContent);

            // Then
            var getResponse = await _client.GetAsync($"/api/blog/{created.Id}");
            getResponse.StatusCode.Should().Be(HttpStatusCode.NotFound);
        }

        [Fact]
        public async Task GetBlogs_ShouldReturnPaginatedResult()
        {
            // Given
            for (int i = 0; i < 20; i++)
            {
                await _client.PostAsJsonAsync("/api/blog", new { title = $"Blog {i}", content = "Test" });

            }

            // When
            var response = await _client.GetAsync("/api/blog?page=1&pageSize=10");
            response.EnsureSuccessStatusCode();

            var result = await response.Content.ReadFromJsonAsync<ApiResponse<List<BlogDto>>>();

            // Then
            result.Should().NotBeNull();
            result.Data.Should().NotBeNull();
            result.Data.Count.Should().Be(10);
        }
    }
}