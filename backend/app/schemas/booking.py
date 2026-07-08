from datetime import datetime

from pydantic import BaseModel


class BookingCreate(BaseModel):
    customer_id: int

    event_type: str

    venue_name: str

    venue_address: str | None = None

    guest_count: int

    budget: float

    advance_paid: float = 0

    event_start: datetime

    event_end: datetime

    setup_start: datetime

    setup_end: datetime

    teardown_start: datetime

    teardown_end: datetime


class BookingResponse(BookingCreate):
    id: int

    remaining_amount: float

    status: str

    class Config:
        from_attributes = True