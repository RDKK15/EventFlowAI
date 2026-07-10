from fastapi import Depends, HTTPException, status

from app.auth.oauth2 import get_current_user
from app.enums.user import UserRole
from app.models.user import User


def require_owner(
    current_user: User = Depends(get_current_user),
):

    if current_user.role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner access required.",
        )

    return current_user


def require_manager(
    current_user: User = Depends(get_current_user),
):

    if current_user.role not in (
        UserRole.OWNER,
        UserRole.MANAGER,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required.",
        )

    return current_user


def require_staff(
    current_user: User = Depends(get_current_user),
):

    if current_user.role not in (
        UserRole.OWNER,
        UserRole.MANAGER,
        UserRole.STAFF,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff access required.",
        )

    return current_user