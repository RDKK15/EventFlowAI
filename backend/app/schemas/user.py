from datetime import datetime

from pydantic import BaseModel

from app.enums.user import UserRole


class UserCreate(BaseModel):
    name: str | None = None
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str | None
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str | None = None
    username: str
    email: str
    is_active: bool


class BusinessUserCreate(BaseModel):
    name: str
    username: str
    email: str
    password: str
    role: UserRole = UserRole.STAFF


class BusinessUserResponse(BaseModel):
    id: int
    business_id: int
    user_id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    user: UserResponse

    class Config:
        from_attributes = True