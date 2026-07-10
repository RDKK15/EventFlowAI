from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)

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
    Enum(UserRole),
    default=UserRole.STAFF,
    nullable=False,
)

    is_active = Column(
        Boolean,
        default=True,
    )