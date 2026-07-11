from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.db.database import get_db
from app.enums.payment import PaymentMethod, PaymentType
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
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=PaymentResponse)
def add_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
):
    return create_payment(db, payment)


@router.get("/", response_model=list[PaymentResponse])
def read_payments(
    payment_code: str | None = None,
    payment_method: PaymentMethod | None = None,
    payment_type: PaymentType | None = None,
    amount_min: float | None = None,
    amount_max: float | None = None,
    payment_date_from: datetime | None = None,
    payment_date_to: datetime | None = None,
    received_by: str | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    return get_payments(
        db=db,
        payment_code=payment_code,
        payment_method=payment_method,
        payment_type=payment_type,
        amount_min=amount_min,
        amount_max=amount_max,
        payment_date_from=payment_date_from,
        payment_date_to=payment_date_to,
        received_by=received_by,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
    )


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