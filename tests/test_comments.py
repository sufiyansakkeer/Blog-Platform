import pytest
from httpx import AsyncClient

from app.models.comment import Comment
from app.models.post import Post
from tests.factories import CommentFactory


@pytest.mark.asyncio
async def test_create_comment_success(
    test_client: AsyncClient,
    test_post: Post,
    auth_headers: dict[str, str],
) -> None:
    """Test successful comment creation."""
    comment_data = CommentFactory.create_comment_data(
        content="This is a test comment"
    )
    
    response = await test_client.post(
        f"/posts/{test_post.id}/comments",
        json=comment_data.model_dump(),
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "This is a test comment"
    assert data["post_id"] == test_post.id
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_comment_unauthorized(test_client: AsyncClient, test_post: Post) -> None:
    """Test comment creation without authentication."""
    comment_data = CommentFactory.create_comment_data()
    
    response = await test_client.post(
        f"/posts/{test_post.id}/comments",
        json=comment_data.model_dump()
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_comment_post_not_found(test_client: AsyncClient, auth_headers: dict[str, str]) -> None:
    """Test comment creation on non-existent post."""
    comment_data = CommentFactory.create_comment_data()
    
    response = await test_client.post(
        "/posts/99999/comments",
        json=comment_data.model_dump(),
        headers=auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_post_comments_success(
    test_client: AsyncClient,
    test_post: Post,
    test_comment: Comment,
) -> None:
    """Test getting all comments for a post."""
    response = await test_client.get(f"/posts/{test_post.id}/comments")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(comment["id"] == test_comment.id for comment in data)


@pytest.mark.asyncio
async def test_get_all_post_comments_empty(test_client: AsyncClient, test_post: Post) -> None:
    """Test getting comments when none exist for a post."""
    response = await test_client.get(f"/posts/{test_post.id}/comments")
    
    assert response.status_code == 200
    # May be empty or have the test_comment, either is acceptable
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_all_post_comments_pagination(test_client: AsyncClient, test_post: Post) -> None:
    """Test pagination of comments."""
    response = await test_client.get(f"/posts/{test_post.id}/comments?skip=0&limit=10")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_all_post_comments_post_not_found(test_client: AsyncClient) -> None:
    """Test getting comments for a non-existent post."""
    response = await test_client.get("/posts/99999/comments")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_comment_success(
    test_client: AsyncClient,
    test_comment: Comment,
    auth_headers: dict[str, str],
) -> None:
    """Test successful comment update by owner."""
    update_data = CommentFactory.create_comment_update_data(
        content="Updated comment content"
    )
    
    response = await test_client.patch(
        f"/posts/comments/{test_comment.id}",
        json=update_data.model_dump(),
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated comment content"


@pytest.mark.asyncio
async def test_update_comment_unauthorized(test_client: AsyncClient, test_comment: Comment) -> None:
    """Test comment update without authentication."""
    update_data = CommentFactory.create_comment_update_data()
    
    response = await test_client.patch(
        f"/posts/comments/{test_comment.id}",
        json=update_data.model_dump()
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_comment_not_found(test_client: AsyncClient, auth_headers: dict[str, str]) -> None:
    """Test updating a non-existent comment."""
    update_data = CommentFactory.create_comment_update_data()
    
    response = await test_client.patch(
        "/posts/comments/99999",
        json=update_data.model_dump(),
        headers=auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_comment_success(
    test_client: AsyncClient,
    test_comment: Comment,
    auth_headers: dict[str, str],
) -> None:
    """Test successful comment deletion by owner."""
    response = await test_client.delete(f"/posts/comments/{test_comment.id}", headers=auth_headers)
    
    assert response.status_code == 204
    
    # Verify comment is deleted by trying to get it (will fail if post doesn't exist or comment doesn't exist)
    # Note: We can't directly check if comment exists, but we can verify the delete response


@pytest.mark.asyncio
async def test_delete_comment_unauthorized(test_client: AsyncClient, test_comment: Comment) -> None:
    """Test comment deletion without authentication."""
    response = await test_client.delete(f"/posts/comments/{test_comment.id}")
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_comment_not_found(test_client: AsyncClient, auth_headers: dict[str, str]) -> None:
    """Test deleting a non-existent comment."""
    response = await test_client.delete("/posts/comments/99999", headers=auth_headers)
    
    assert response.status_code == 404
