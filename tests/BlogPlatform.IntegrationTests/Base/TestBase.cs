using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogPlatform.IntegrationTests.Factories;

namespace BlogPlatform.IntegrationTests.Base
{
    public class TestBase : IClassFixture<CustomWebApplicationFactory>
    {
        protected readonly HttpClient _client;
        public TestBase(CustomWebApplicationFactory factory)
        {
            _client = factory.CreateClient();

        }
    }
}