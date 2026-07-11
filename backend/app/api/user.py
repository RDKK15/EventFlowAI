from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.permissions import require_owner
from app.db.database import get_db
from app.enums.user import UserRole
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import (
    get_users,
    get_user_by_id,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=list[UserResponse],
)
def read_users(
    username: str | None = None,
    email: str | None = None,
    role: UserRole | None = None,
    is_active: bool | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    return get_users(
        db=db,
        username=username,
        email=email,
        role=role,
        is_active=is_active,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    return get_user_by_id(
        db,
        user_id,
    )