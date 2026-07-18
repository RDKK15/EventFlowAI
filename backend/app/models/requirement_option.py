from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class RequirementOption(Base):
    __tablename__ = "requirement_options"

    __table_args__ = (
        UniqueConstraint(
            "requirement_definition_id",
            "value",
            name="uq_requirement_options_definition_value",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    requirement_definition_id = Column(
        Integer,
        ForeignKey("requirement_definitions.id"),
        nullable=False,
        index=True,
    )

    value = Column(
        String,
        nullable=False,
    )

    label = Column(
        String,
        nullable=False,
    )

    display_order = Column(
        Integer,
        nullable=False,
        default=0,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    requirement_definition = relationship(
        "RequirementDefinition",
        back_populates="options",
    )