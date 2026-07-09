from datetime import datetime

from pydantic import BaseModel

from app.enums.payment import PaymentMethod, PaymentType


class PaymentCreate(BaseModel):
    booking_id: int

    amount: float

    payment_type: PaymentType

    payment_method: PaymentMethod

    payment_date: datetime

    reference_number: str | None = None

    received_by: str

    notes: str | None = None


class PaymentUpdate(BaseModel):
    booking_id: int

    amount: float

    payment_type: PaymentType

    payment_method: PaymentMethod

    payment_date: datetime

    reference_number: str | None = None

    received_by: str

    notes: str | None = None


class PaymentResponse(PaymentCreate):
    id: int

    payment_code: str

    class Config:
        from_attributes = True