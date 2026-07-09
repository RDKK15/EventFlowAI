from datetime import date

from pydantic import BaseModel


class QuotationCreate(BaseModel):
    enquiry_id: int

    total_amount: int

    discount: int = 0

    valid_until: date | None = None

    notes: str | None = None


class QuotationUpdate(BaseModel):
    enquiry_id: int

    total_amount: int

    discount: int = 0

    valid_until: date | None = None

    notes: str | None = None


class QuotationResponse(BaseModel):
    id: int

    quotation_code: str

    enquiry_id: int

    total_amount: int

    discount: int

    final_amount: int

    valid_until: date | None = None

    status: str

    notes: str | None = None

    class Config:
        from_attributes = True