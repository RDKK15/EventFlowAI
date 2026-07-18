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


class ServiceType(Base):
    __tablename__ = "service_types"

    __table_args__ = (
        UniqueConstraint(
            "business_id",
            "name",
            name="uq_service_types_business_name",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    description = Column(
        String,
        nullable=True,
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

    business = relationship(
        "Business",
        back_populates="service_types",
    )

    requirement_definitions = relationship(
       "RequirementDefinition",
       back_populates="service_type",
       order_by="RequirementDefinition.display_order",
)