from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.db.database import Base

from sqlalchemy import Enum
from app.enums.user import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Nullable for Phase 1: the existing /auth/register flow and the
    # default-owner bootstrap (app/startup/initialize.py) create users
    # with no business context yet. Making this NOT NULL now would break
    # both. It becomes the ownership boundary once business-aware user
    # creation (POST /businesses/{business_id}/users) is used, or once
    # auth itself becomes business-aware.
    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=True,
        index=True,
    )

    name = Column(
        String,
        nullable=True,
    )

    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
    )

    hashed_password = Column(
        String,
        nullable=False,
    )


    role = Column(
    Enum(
        UserRole,
        values_callable=lambda enum: [e.value for e in enum],
    ),
    default=UserRole.STAFF.value,
    nullable=False,
)

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    business = relationship(
        "Business",
        back_populates="users",
    )