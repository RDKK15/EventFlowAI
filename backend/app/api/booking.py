from fastapi import APIRouter, Depends
from app.auth.oauth2 import get_current_user
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingResponse,
)
from app.services.booking_service import (
    create_booking,
    get_bookings,
    get_booking_by_id,
    update_booking,
    delete_booking,
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=BookingResponse)
def add_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
):
    return create_booking(db, booking)


@router.get("/", response_model=list[BookingResponse])
def read_bookings(
    db: Session = Depends(get_db),
):
    return get_bookings(db)


@router.get("/{booking_id}", response_model=BookingResponse)
def read_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):
    return get_booking_by_id(
        db,
        booking_id,
    )


@router.put("/{booking_id}", response_model=BookingResponse)
def edit_booking(
    booking_id: int,
    booking: BookingUpdate,
    db: Session = Depends(get_db),
):
    return update_booking(
        db,
        booking_id,
        booking,
    )


@router.delete("/{booking_id}")
def remove_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):
    return delete_booking(
        db,
        booking_id,
    )