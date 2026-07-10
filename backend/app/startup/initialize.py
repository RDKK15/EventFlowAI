from sqlalchemy.orm import Session

from app.models.user import User
from app.enums.user import UserRole
from app.auth.security import hash_password


def create_default_owner(db: Session):
    owner = (
        db.query(User)
        .filter(User.role == UserRole.OWNER.value)
        .first()
    )

    if owner:
        print("✓ Default owner already exists.")
        return

    owner = User(
        username="owner",
        email="owner@bizpart.ai",
        hashed_password=hash_password("password123"),
        role=UserRole.OWNER.value,
        is_active=True,
    )

    db.add(owner)
    db.commit()

    print("✓ Default owner created.")