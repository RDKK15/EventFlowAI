from datetime import datetime

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


class BusinessUserCreate(BaseModel):
    """
    Used for business-scoped user creation (POST /businesses/{business_id}/users).

    business_id is intentionally NOT a field here: it cannot be
    overridden via the JSON body, it always comes from the URL path.
    That said, the URL path is still client-controlled input, not a
    trusted tenant/auth context -- this endpoint is DEV/BOOTSTRAP-ONLY
    for Phase 1 and does not enforce that the caller is authorized for
    that business_id. See the TODO in app/api/business.py. The real fix
    is deriving business_id from current_user.business_id once
    business-aware auth exists, not from any client-supplied input.
    """

    name: str
    username: str
    email: str
    password: str
    role: UserRole = UserRole.STAFF


class BusinessUserResponse(BaseModel):
    id: int
    business_id: int | None
    name: str | None
    username: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True