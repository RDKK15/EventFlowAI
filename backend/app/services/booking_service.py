from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.quotation import Quotation
from app.schemas.booking import BookingCreate
from app.utils.code_generator import generate_code


def create_booking(db: Session, booking: BookingCreate):

    # Check quotation exists
    quotation = (
        db.query(Quotation)
        .filter(Quotation.id == booking.quotation_id)
        .first()
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found."
        )

    # Business validations
    if booking.setup_end >= booking.event_start:
        raise HTTPException(
            status_code=400,
            detail="Setup must finish before the event starts."
        )

    if booking.event_end <= booking.event_start:
        raise HTTPException(
            status_code=400,
            detail="Event end must be after event start."
        )

    if booking.teardown_start < booking.event_end:
        raise HTTPException(
            status_code=400,
            detail="Teardown can only start after the event ends."
        )

    # Create booking
    new_booking = Booking(
        quotation_id=booking.quotation_id,
        venue_name=booking.venue_name,
        venue_address=booking.venue_address,
        advance_paid=booking.advance_paid,
        setup_start=booking.setup_start,
        setup_end=booking.setup_end,
        event_start=booking.event_start,
        event_end=booking.event_end,
        teardown_start=booking.teardown_start,
        teardown_end=booking.teardown_end,
        notes=booking.notes
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # Generate friendly booking code
    new_booking.booking_code = generate_code(
        "B",
        new_booking.id
    )

    db.commit()
    db.refresh(new_booking)

    return new_booking


def get_bookings(db: Session):
    return db.query(Booking).all()