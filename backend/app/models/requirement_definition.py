from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.enums.requirement import (
    RequirementCollectionStage,
    RequirementValueType,
)


class RequirementDefinition(Base):
    __tablename__ = "requirement_definitions"

    __table_args__ = (
        UniqueConstraint(
            "service_type_id",
            "key",
            name="uq_requirement_definitions_service_key",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    service_type_id = Column(
        Integer,
        ForeignKey("service_types.id"),
        nullable=False,
        index=True,
    )

    key = Column(
        String,
        nullable=False,
    )

    label = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    value_type = Column(
        Enum(
            RequirementValueType,
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
    )

    unit = Column(
        String,
        nullable=True,
    )

    is_required = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    ask_customer = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    collection_stage = Column(
        Enum(
            RequirementCollectionStage,
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
        default=RequirementCollectionStage.ENQUIRY.value,
    )

    display_order = Column(
        Integer,
        nullable=False,
        default=0,
    )

    ai_hint = Column(
        Text,
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

    service_type = relationship(
        "ServiceType",
        back_populates="requirement_definitions",
    )

    options = relationship(
        "RequirementOption",
        back_populates="requirement_definition",
        order_by="RequirementOption.display_order",
    )