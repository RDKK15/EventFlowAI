from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr | None = None


class CustomerUpdate(BaseModel):
    name: str
    phone: str
    email: EmailStr | None = None


class CustomerResponse(CustomerCreate):
    id: int
    customer_code: str

    class Config:
        from_attributes = True