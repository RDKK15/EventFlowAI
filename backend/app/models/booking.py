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
from app.enums.booking import BookingStatus


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    booking_code = Column(String, unique=True, index=True)

    quotation_id = Column(Integer, ForeignKey("quotations.id"))

    venue_name = Column(String, nullable=False)

    venue_address = Column(String)

    advance_paid = Column(Float, default=0)

    setup_start = Column(DateTime)
    setup_end = Column(DateTime)

    event_start = Column(DateTime)
    event_end = Column(DateTime)

    teardown_start = Column(DateTime)
    teardown_end = Column(DateTime)

    booking_status = Column(
        Enum(BookingStatus),
        default=BookingStatus.PROPOSAL,
        nullable=False,
    )

    notes = Column(String)

    quotation = relationship(
        "Quotation",
        back_populates="booking"
    )

    payments = relationship(
        "Payment",
        back_populates="booking"
    )