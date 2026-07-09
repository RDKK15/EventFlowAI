from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
)
from app.services.payment_service import (
    create_payment,
    get_payments,
    get_payment_by_id,
    update_payment,
    delete_payment,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post("/", response_model=PaymentResponse)
def add_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
):
    return create_payment(db, payment)


@router.get("/", response_model=list[PaymentResponse])
def read_payments(
    db: Session = Depends(get_db),
):
    return get_payments(db)


@router.get("/{payment_id}", response_model=PaymentResponse)
def read_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):
    return get_payment_by_id(
        db,
        payment_id,
    )


@router.put("/{payment_id}", response_model=PaymentResponse)
def edit_payment(
    payment_id: int,
    payment: PaymentUpdate,
    db: Session = Depends(get_db),
):
    return update_payment(
        db,
        payment_id,
        payment,
    )


@router.delete("/{payment_id}")
def remove_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):
    return delete_payment(
        db,
        payment_id,
    )