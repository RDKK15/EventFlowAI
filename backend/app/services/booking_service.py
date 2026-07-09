from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.quotation import Quotation
from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
)
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

    new_booking.booking_code = generate_code(
        "B",
        new_booking.id
    )

    db.commit()
    db.refresh(new_booking)

    return new_booking


def get_bookings(db: Session):
    return db.query(Booking).all()


def get_booking_by_id(
    db: Session,
    booking_id: int,
):
    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )

    return booking


def update_booking(
    db: Session,
    booking_id: int,
    booking_data: BookingUpdate,
):

    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )

    quotation = (
        db.query(Quotation)
        .filter(Quotation.id == booking_data.quotation_id)
        .first()
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found."
        )

    # Business validations
    if booking_data.setup_end >= booking_data.event_start:
        raise HTTPException(
            status_code=400,
            detail="Setup must finish before the event starts."
        )

    if booking_data.event_end <= booking_data.event_start:
        raise HTTPException(
            status_code=400,
            detail="Event end must be after event start."
        )

    if booking_data.teardown_start < booking_data.event_end:
        raise HTTPException(
            status_code=400,
            detail="Teardown can only start after the event ends."
        )

    booking.quotation_id = booking_data.quotation_id
    booking.venue_name = booking_data.venue_name
    booking.venue_address = booking_data.venue_address
    booking.advance_paid = booking_data.advance_paid
    booking.setup_start = booking_data.setup_start
    booking.setup_end = booking_data.setup_end
    booking.event_start = booking_data.event_start
    booking.event_end = booking_data.event_end
    booking.teardown_start = booking_data.teardown_start
    booking.teardown_end = booking_data.teardown_end
    booking.notes = booking_data.notes

    db.commit()
    db.refresh(booking)

    return booking


def delete_booking(
    db: Session,
    booking_id: int,
):

    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )

    if booking.payments:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete booking with existing payments."
        )

    db.delete(booking)
    db.commit()

    return {
        "message": "Booking deleted successfully."
    }