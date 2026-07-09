from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)
from app.services.customer_service import (
    create_customer,
    get_customers,
    get_customer_by_id,
    update_customer,
    delete_customer,
)

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerResponse)
def add_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)


@router.get("/", response_model=list[CustomerResponse])
def read_customers(db: Session = Depends(get_db)):
    return get_customers(db)

@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    return get_customer_by_id(db, customer_id)

@router.put("/{customer_id}", response_model=CustomerResponse)
def edit_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
):
    return update_customer(
        db,
        customer_id,
        customer,
    )

@router.delete("/{customer_id}")
def remove_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    return delete_customer(
        db,
        customer_id,
    )