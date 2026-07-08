from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import (
    create_booking,
    get_bookings,
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
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