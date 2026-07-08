from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.db.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    event_type = Column(String, nullable=False)

    venue_name = Column(String, nullable=False)

    venue_address = Column(String)

    guest_count = Column(Integer)

    budget = Column(Float)

    advance_paid = Column(Float, default=0)

    remaining_amount = Column(Float)

    event_start = Column(DateTime)

    event_end = Column(DateTime)

    setup_start = Column(DateTime)

    setup_end = Column(DateTime)

    teardown_start = Column(DateTime)

    teardown_end = Column(DateTime)

    status = Column(String, default="Pending")