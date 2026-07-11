from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class BusinessSequence(Base):
    """
    Tracks an independent, per-business counter used to generate
    human-friendly display codes (e.g. EVT-0001, CUS-0001).

    Each (business_id, sequence_type) pair has exactly one row, enforced
    by a unique constraint. Different businesses may reach the same
    display code independently (e.g. two businesses can each have their
    own EVT-0001) because the counter is scoped per business.
    """

    __tablename__ = "business_sequences"

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

    # Stored as a plain string rather than a DB enum on purpose: new
    # sequence types (CUSTOMER, EVENT, QUOTATION, PAYMENT, ...) will be
    # added as future domain models land, and a string column lets that
    # happen without an Alembic migration each time. Application code
    # should still reference the known types via app.enums.sequence.SequenceType
    # for type safety when calling the sequence service.
    sequence_type = Column(
        String,
        nullable=False,
    )

    current_value = Column(
        Integer,
        nullable=False,
        default=0,
    )

    business = relationship(
        "Business",
        back_populates="sequences",
    )

    __table_args__ = (
        UniqueConstraint(
            "business_id",
            "sequence_type",
            name="uq_business_sequence_business_id_sequence_type",
        ),
    )
