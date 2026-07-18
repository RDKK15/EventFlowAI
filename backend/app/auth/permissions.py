from fastapi import Depends, HTTPException, status

from app.auth.tenant import (
    BusinessContext,
    get_business_context,
)
from app.enums.user import UserRole


def require_owner(
    context: BusinessContext = Depends(get_business_context),
) -> BusinessContext:

    if context.membership.role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner access required.",
        )

    return context


def require_manager(
    context: BusinessContext = Depends(get_business_context),
) -> BusinessContext:

    if context.membership.role not in (
        UserRole.OWNER,
        UserRole.MANAGER,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required.",
        )

    return context


def require_staff(
    context: BusinessContext = Depends(get_business_context),
) -> BusinessContext:

    if context.membership.role not in (
        UserRole.OWNER,
        UserRole.MANAGER,
        UserRole.STAFF,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff access required.",
        )

    return context