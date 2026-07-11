from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.enums.user import UserRole
from app.models.business import Business
from app.models.user import User
from app.schemas.user import BusinessUserCreate

from app.utils.query_utils import (
    apply_sorting,
    apply_pagination,
)


def get_users(
    db: Session,
    username: str | None = None,
    email: str | None = None,
    role: UserRole | None = None,
    is_active: bool | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
):

    query = db.query(User)

    # Username
    if username:
        query = query.filter(
            User.username.ilike(f"%{username}%")
        )

    # Email
    if email:
        query = query.filter(
            User.email.ilike(f"%{email}%")
        )

    # Role
    if role:
        query = query.filter(
            User.role == role
        )

    # Active / Inactive
    if is_active is not None:
        query = query.filter(
            User.is_active == is_active
        )

    # Allowed sorting columns
    allowed_columns = {
        "id": User.id,
        "username": User.username,
        "email": User.email,
        "role": User.role,
        "is_active": User.is_active,
    }

    query = apply_sorting(
        query,
        allowed_columns,
        sort_by,
        order,
    )

    query = apply_pagination(
        query,
        page,
        limit,
    )

    return query.all()


def get_user_by_id(
    db: Session,
    user_id: int,
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return user


def update_user(
    db: Session,
    user_id: int,
    user_data,
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    existing_username = (
        db.query(User)
        .filter(
            User.username == user_data.username,
            User.id != user_id,
        )
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists.",
        )

    existing_email = (
        db.query(User)
        .filter(
            User.email == user_data.email,
            User.id != user_id,
        )
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists.",
        )

    user.username = user_data.username
    user.email = user_data.email
    user.role = user_data.role
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return user


def create_business_user(
    db: Session,
    business_id: int,
    user_data: BusinessUserCreate,
) -> User:
    """
    Business-aware user creation. business_id comes from the caller
    (the API route takes it from the URL path, not from the request
    body), so this never lets a client choose an arbitrary business_id
    via the JSON body specifically.

    DEV/BOOTSTRAP-ONLY CAVEAT: the URL path itself is still a
    client-controlled input, not a trusted tenant context -- see the
    TODO in app/api/business.py. This function does not enforce that
    the caller is actually authorized for `business_id`; there is no
    authenticated tenant context to check against yet in Phase 1.
    """

    business = (
        db.query(Business)
        .filter(Business.id == business_id)
        .first()
    )

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found.",
        )

    existing_username = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists.",
        )

    existing_email = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists.",
        )

    new_user = User(
        business_id=business.id,
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_users_by_business(
    db: Session,
    business_id: int,
):
    return (
        db.query(User)
        .filter(User.business_id == business_id)
        .all()
    )