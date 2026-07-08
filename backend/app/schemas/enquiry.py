from datetime import date
from pydantic import BaseModel


class EnquiryCreate(BaseModel):
    customer_id: int
    event_type: str
    preferred_date: date
    flexible_date: bool = False

    venue_confirmed: bool = False
    venue_name: str | None = None
    venue_address: str | None = None

    guest_count: int

    budget_min: int | None = None
    budget_max: int | None = None

    decoration_theme: str | None = None

    lead_source: str

    notes: str | None = None


class EnquiryResponse(EnquiryCreate):
    id: int
    stage: str

    class Config:
        from_attributes = True