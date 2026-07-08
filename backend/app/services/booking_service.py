from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.schemas.booking import BookingCreate


def create_booking(db: Session, booking: BookingCreate):

    remaining_amount = booking.budget - booking.advance_paid

    new_booking = Booking(
        customer_id=booking.customer_id,
        event_type=booking.event_type,
        venue_name=booking.venue_name,
        venue_address=booking.venue_address,
        guest_count=booking.guest_count,
        budget=booking.budget,
        advance_paid=booking.advance_paid,
        remaining_amount=remaining_amount,
        event_start=booking.event_start,
        event_end=booking.event_end,
        setup_start=booking.setup_start,
        setup_end=booking.setup_end,
        teardown_start=booking.teardown_start,
        teardown_end=booking.teardown_end,
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


def get_bookings(db: Session):
    return db.query(Booking).all()