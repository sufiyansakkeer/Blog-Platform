from faker import Faker
from app.schemas.user import UserCreate, UserLogin
from app.schemas.post import PostCreate, PostUpdate
from app.schemas.comment import CommentCreate, CommentUpdate

fake = Faker()


class UserFactory:
    """Factory for creating user test data."""
    
    @staticmethod
    def create_user_data(
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> UserCreate:
        """Create a UserCreate object with fake data."""
        return UserCreate(
            username=username or fake.user_name(),
            email=email or fake.email(),
            password=password or fake.password(length=12, special_chars=True, digits=True, upper_case=True),
        )
    
    @staticmethod
    def create_login_data(
        email: str | None = None,
        password: str | None = None,
    ) -> UserLogin:
        """Create a UserLogin object with fake data."""
        return UserLogin(
            email=email or fake.email(),
            password=password or fake.password(length=12, special_chars=True, digits=True, upper_case=True),
        )


class PostFactory:
    """Factory for creating post test data."""
    
    @staticmethod
    def create_post_data(
        title: str | None = None,
        content: str | None = None,
    ) -> PostCreate:
        """Create a PostCreate object with fake data."""
        return PostCreate(
            title=title or fake.sentence(nb_words=6),
            content=content or fake.paragraph(nb_sentences=5),
        )
    
    @staticmethod
    def create_post_update_data(
        title: str | None = None,
        content: str | None = None,
    ) -> PostUpdate:
        """Create a PostUpdate object with fake data."""
        return PostUpdate(
            title=title or fake.sentence(nb_words=6),
            content=content or fake.paragraph(nb_sentences=5),
        )


class CommentFactory:
    """Factory for creating comment test data."""
    
    @staticmethod
    def create_comment_data(
        content: str | None = None,
    ) -> CommentCreate:
        """Create a CommentCreate object with fake data."""
        return CommentCreate(
            content=content or fake.paragraph(nb_sentences=2),
        )
    
    @staticmethod
    def create_comment_update_data(
        content: str | None = None,
    ) -> CommentUpdate:
        """Create a CommentUpdate object with fake data."""
        return CommentUpdate(
            content=content or fake.paragraph(nb_sentences=2),
        )
