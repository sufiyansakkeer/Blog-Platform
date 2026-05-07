import pytest
from httpx import AsyncClient

from app.models.post import Post
from tests.factories import PostFactory


@pytest.mark.asyncio
async def test_create_post_success(
    test_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Test successful post creation."""
    post_data = PostFactory.create_post_data(
        title="My Test Post",
        content="This is the content of my test post"
    )
    
    response = await test_client.post("/posts", json=post_data.model_dump(), headers=auth_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Test Post"
    assert data["content"] == "This is the content of my test post"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_post_unauthorized(test_client: AsyncClient) -> None:
    """Test post creation without authentication."""
    post_data = PostFactory.create_post_data()
    
    response = await test_client.post("/posts", json=post_data.model_dump())
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_all_posts_empty(test_client: AsyncClient) -> None:
    """Test getting all posts when none exist."""
    response = await test_client.get("/posts")
    
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_all_posts_success(
    test_client: AsyncClient,
    test_post: Post,
) -> None:
    """Test getting all posts with existing posts."""
    response = await test_client.get("/posts")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(post["id"] == test_post.id for post in data)


@pytest.mark.asyncio
async def test_get_all_posts_pagination(test_client: AsyncClient, test_post: Post) -> None:
    """Test pagination of posts."""
    response = await test_client.get("/posts?skip=0&limit=10")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_post_by_id_success(
    test_client: AsyncClient,
    test_post: Post,
) -> None:
    """Test getting a specific post by ID."""
    response = await test_client.get(f"/posts/{test_post.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_post.id
    assert data["title"] == test_post.title
    assert data["content"] == test_post.content


@pytest.mark.asyncio
async def test_get_post_by_id_not_found(test_client: AsyncClient) -> None:
    """Test getting a non-existent post."""
    response = await test_client.get("/posts/99999")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_post_success(
    test_client: AsyncClient,
    test_post: Post,
    auth_headers: dict[str, str],
) -> None:
    """Test successful post update by owner."""
    update_data = PostFactory.create_post_update_data(
        title="Updated Title",
        content="Updated content"
    )
    
    response = await test_client.patch(
        f"/posts/{test_post.id}",
        json=update_data.model_dump(),
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"


@pytest.mark.asyncio
async def test_update_post_unauthorized(test_client: AsyncClient, test_post: Post) -> None:
    """Test post update without authentication."""
    update_data = PostFactory.create_post_update_data()
    
    response = await test_client.patch(
        f"/posts/{test_post.id}",
        json=update_data.model_dump()
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_post_not_found(test_client: AsyncClient, auth_headers: dict[str, str]) -> None:
    """Test updating a non-existent post."""
    update_data = PostFactory.create_post_update_data()
    
    response = await test_client.patch(
        "/posts/99999",
        json=update_data.model_dump(),
        headers=auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_post_success(
    test_client: AsyncClient,
    test_post: Post,
    auth_headers: dict[str, str],
) -> None:
    """Test successful post deletion by owner."""
    response = await test_client.delete(f"/posts/{test_post.id}", headers=auth_headers)
    
    assert response.status_code == 204
    
    # Verify post is deleted
    get_response = await test_client.get(f"/posts/{test_post.id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_post_unauthorized(test_client: AsyncClient, test_post: Post) -> None:
    """Test post deletion without authentication."""
    response = await test_client.delete(f"/posts/{test_post.id}")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_post_not_found(test_client: AsyncClient, auth_headers: dict[str, str]) -> None:
    """Test deleting a non-existent post."""
    response = await test_client.delete("/posts/99999", headers=auth_headers)
    
    assert response.status_code == 404
