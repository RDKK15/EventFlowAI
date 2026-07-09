from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.enums.payment import PaymentMethod, PaymentType


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    payment_code = Column(String, unique=True, index=True)

    booking_id = Column(Integer, ForeignKey("bookings.id"))

    amount = Column(Float, nullable=False)

    payment_type = Column(
        Enum(PaymentType),
        nullable=False,
    )

    payment_method = Column(
        Enum(PaymentMethod),
        nullable=False,
    )

    payment_date = Column(DateTime, nullable=False)

    reference_number = Column(String)

    received_by = Column(String, nullable=False)

    notes = Column(String)

    booking = relationship(
        "Booking",
        back_populates="payments"
    )