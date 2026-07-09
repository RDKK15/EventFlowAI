from datetime import datetime

from pydantic import BaseModel

from app.enums.booking import BookingStatus


class BookingCreate(BaseModel):
    quotation_id: int

    venue_name: str

    venue_address: str | None = None

    advance_paid: float = 0

    setup_start: datetime
    setup_end: datetime

    event_start: datetime
    event_end: datetime

    teardown_start: datetime
    teardown_end: datetime

    notes: str | None = None


class BookingUpdate(BaseModel):
    quotation_id: int

    venue_name: str

    venue_address: str | None = None

    advance_paid: float = 0

    setup_start: datetime
    setup_end: datetime

    event_start: datetime
    event_end: datetime

    teardown_start: datetime
    teardown_end: datetime

    notes: str | None = None


class BookingResponse(BookingCreate):
    id: int

    booking_code: str

    booking_status: BookingStatus

    class Config:
        from_attributes = True