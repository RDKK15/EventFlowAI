from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import (
    get_users,
    get_user_by_id,
)
from app.auth.permissions import require_owner


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=list[UserResponse],
)
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    return get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    return get_user_by_id(db, user_id)