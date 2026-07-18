from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.enums.user import UserRole
from app.models.business import Business
from app.models.business_user import BusinessUser
from app.models.user import User


def create_default_owner(db: Session):

    business = (
        db.query(Business)
        .filter(Business.business_code == "DEFAULT")
        .first()
    )

    if business is None:
        business = Business(
            name="Default Business",
            business_code="DEFAULT",
            is_active=True,
        )

        db.add(business)
        db.flush()

    owner = (
        db.query(User)
        .filter(User.username == "owner")
        .first()
    )

    if owner is None:
        owner = User(
            name="Default Owner",
            username="owner",
            email="owner@bizpart.ai",
            hashed_password=hash_password("password123"),
            is_active=True,
        )

        db.add(owner)
        db.flush()

    membership = (
        db.query(BusinessUser)
        .filter(
            BusinessUser.business_id == business.id,
            BusinessUser.user_id == owner.id,
        )
        .first()
    )

    if membership is None:
        membership = BusinessUser(
            business_id=business.id,
            user_id=owner.id,
            role=UserRole.OWNER,
            is_active=True,
        )

        db.add(membership)

    db.commit()

    print("✓ Default business and owner membership ready.")