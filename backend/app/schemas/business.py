from datetime import datetime

from pydantic import BaseModel


class BusinessCreate(BaseModel):
    name: str
    business_code: str | None = None


class BusinessResponse(BaseModel):
    id: int
    name: str
    business_code: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
