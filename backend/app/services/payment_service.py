from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.payment import Payment
from app.models.quotation import Quotation
from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
)
from app.utils.code_generator import generate_code

from app.utils.query_utils import (
    apply_sorting,
    apply_pagination,
)


def create_payment(
    db: Session,
    payment: PaymentCreate,
):

    booking = (
        db.query(Booking)
        .filter(Booking.id == payment.booking_id)
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )

    quotation = (
        db.query(Quotation)
        .filter(Quotation.id == booking.quotation_id)
        .first()
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found."
        )

    if payment.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Payment amount must be greater than zero."
        )

    total_paid = (
        db.query(func.sum(Payment.amount))
        .filter(Payment.booking_id == payment.booking_id)
        .scalar()
    ) or 0

    if total_paid + payment.amount > quotation.final_amount:
        raise HTTPException(
            status_code=400,
            detail="Payment exceeds remaining balance."
        )

    new_payment = Payment(
        booking_id=payment.booking_id,
        amount=payment.amount,
        payment_type=payment.payment_type,
        payment_method=payment.payment_method,
        payment_date=payment.payment_date,
        reference_number=payment.reference_number,
        received_by=payment.received_by,
        notes=payment.notes,
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    new_payment.payment_code = generate_code(
        "P",
        new_payment.id,
    )

    db.commit()
    db.refresh(new_payment)

    return new_payment


def get_payments(
    db: Session,
    payment_code: str | None = None,
    payment_method=None,
    payment_type=None,
    amount_min: float | None = None,
    amount_max: float | None = None,
    payment_date_from=None,
    payment_date_to=None,
    received_by: str | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
):

    query = db.query(Payment)

    # Payment Code
    if payment_code:
        query = query.filter(
            Payment.payment_code.ilike(f"%{payment_code}%")
        )

    # Payment Method
    if payment_method:
        query = query.filter(
            Payment.payment_method == payment_method
        )

    # Payment Type
    if payment_type:
        query = query.filter(
            Payment.payment_type == payment_type
        )

    # Received By
    if received_by:
        query = query.filter(
            Payment.received_by.ilike(f"%{received_by}%")
        )

    # Amount Min
    if amount_min is not None:
        query = query.filter(
            Payment.amount >= amount_min
        )

    # Amount Max
    if amount_max is not None:
        query = query.filter(
            Payment.amount <= amount_max
        )

    # Payment Date From
    if payment_date_from:
        query = query.filter(
            Payment.payment_date >= payment_date_from
        )

    # Payment Date To
    if payment_date_to:
        query = query.filter(
            Payment.payment_date <= payment_date_to
        )

    allowed_columns = {
        "id": Payment.id,
        "payment_code": Payment.payment_code,
        "amount": Payment.amount,
        "payment_date": Payment.payment_date,
        "received_by": Payment.received_by,
    }

    query = apply_sorting(
        query,
        allowed_columns,
        sort_by,
        order,
    )

    query = apply_pagination(
        query,
        page,
        limit,
    )

    return query.all()


def get_payment_by_id(
    db: Session,
    payment_id: int,
):

    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id)
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found."
        )

    return payment

def update_payment(
    db: Session,
    payment_id: int,
    payment_data: PaymentUpdate,
):

    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id)
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found."
        )

    booking = (
        db.query(Booking)
        .filter(Booking.id == payment_data.booking_id)
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )

    quotation = (
        db.query(Quotation)
        .filter(Quotation.id == booking.quotation_id)
        .first()
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found."
        )

    if payment_data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Payment amount must be greater than zero."
        )

    total_paid = (
        db.query(func.sum(Payment.amount))
        .filter(
            Payment.booking_id == payment_data.booking_id,
            Payment.id != payment_id,
        )
        .scalar()
    ) or 0

    if total_paid + payment_data.amount > quotation.final_amount:
        raise HTTPException(
            status_code=400,
            detail="Payment exceeds remaining balance."
        )

    payment.booking_id = payment_data.booking_id
    payment.amount = payment_data.amount
    payment.payment_type = payment_data.payment_type
    payment.payment_method = payment_data.payment_method
    payment.payment_date = payment_data.payment_date
    payment.reference_number = payment_data.reference_number
    payment.received_by = payment_data.received_by
    payment.notes = payment_data.notes

    db.commit()
    db.refresh(payment)

    return payment


def delete_payment(
    db: Session,
    payment_id: int,
):

    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id)
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found."
        )

    db.delete(payment)
    db.commit()

    return {
        "message": "Payment deleted successfully."
    }