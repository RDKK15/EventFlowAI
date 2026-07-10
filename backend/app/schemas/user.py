from pydantic import BaseModel

from app.enums.user import UserRole


from app.enums.user import UserRole

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.STAFF


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool

class UserUpdate(BaseModel):
    username: str
    email: str
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True