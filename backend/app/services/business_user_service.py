from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.auth.security import hash_password
from app.models.business import Business
from app.models.business_user import BusinessUser
from app.models.user import User
from app.schemas.user import BusinessUserCreate


def create_business_user(
    db: Session,
    business_id: int,
    user_data: BusinessUserCreate,
) -> BusinessUser:

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
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_active=True,
    )

    db.add(new_user)
    db.flush()

    membership = BusinessUser(
        business_id=business.id,
        user_id=new_user.id,
        role=user_data.role,
        is_active=True,
    )

    db.add(membership)
    db.commit()
    db.refresh(membership)

    return (
        db.query(BusinessUser)
        .options(joinedload(BusinessUser.user))
        .filter(BusinessUser.id == membership.id)
        .first()
    )


def get_users_by_business(
    db: Session,
    business_id: int,
) -> list[BusinessUser]:

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

    return (
        db.query(BusinessUser)
        .options(joinedload(BusinessUser.user))
        .filter(
            BusinessUser.business_id == business_id,
        )
        .all()
    )