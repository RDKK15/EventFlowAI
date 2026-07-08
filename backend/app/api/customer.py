from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import create_customer, get_customers

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerResponse)
def add_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)


@router.get("/", response_model=list[CustomerResponse])
def read_customers(db: Session = Depends(get_db)):
    return get_customers(db)