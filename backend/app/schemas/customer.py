from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr | None = None


class CustomerResponse(CustomerCreate):
    id: int

    class Config:
        from_attributes = True