from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool


class UserLogin(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str
