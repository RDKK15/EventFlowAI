from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.enquiry import Enquiry
from app.models.quotation import Quotation
from app.schemas.quotation import (
    QuotationCreate,
    QuotationUpdate,
)
from app.utils.code_generator import generate_code


def create_quotation(db: Session, quotation: QuotationCreate):

    enquiry = (
        db.query(Enquiry)
        .filter(Enquiry.id == quotation.enquiry_id)
        .first()
    )

    if not enquiry:
        raise HTTPException(
            status_code=404,
            detail="Enquiry not found."
        )

    if quotation.total_amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Total amount must be greater than zero."
        )

    if quotation.discount < 0:
        raise HTTPException(
            status_code=400,
            detail="Discount cannot be negative."
        )

    if quotation.discount > quotation.total_amount:
        raise HTTPException(
            status_code=400,
            detail="Discount cannot exceed total amount."
        )

    final_amount = quotation.total_amount - quotation.discount

    new_quotation = Quotation(
        enquiry_id=quotation.enquiry_id,
        total_amount=quotation.total_amount,
        discount=quotation.discount,
        final_amount=final_amount,
        valid_until=quotation.valid_until,
        notes=quotation.notes
    )

    db.add(new_quotation)
    db.commit()
    db.refresh(new_quotation)

    new_quotation.quotation_code = generate_code(
        "Q",
        new_quotation.id
    )

    db.commit()
    db.refresh(new_quotation)

    return new_quotation


def get_quotations(db: Session):
    return db.query(Quotation).all()


def get_quotation_by_id(
    db: Session,
    quotation_id: int,
):
    quotation = (
        db.query(Quotation)
        .filter(Quotation.id == quotation_id)
        .first()
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found."
        )

    return quotation


def update_quotation(
    db: Session,
    quotation_id: int,
    quotation_data: QuotationUpdate,
):
    quotation = (
        db.query(Quotation)
        .filter(Quotation.id == quotation_id)
        .first()
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found."
        )

    enquiry = (
        db.query(Enquiry)
        .filter(Enquiry.id == quotation_data.enquiry_id)
        .first()
    )

    if not enquiry:
        raise HTTPException(
            status_code=404,
            detail="Enquiry not found."
        )

    if quotation_data.total_amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Total amount must be greater than zero."
        )

    if quotation_data.discount < 0:
        raise HTTPException(
            status_code=400,
            detail="Discount cannot be negative."
        )

    if quotation_data.discount > quotation_data.total_amount:
        raise HTTPException(
            status_code=400,
            detail="Discount cannot exceed total amount."
        )

    quotation.enquiry_id = quotation_data.enquiry_id
    quotation.total_amount = quotation_data.total_amount
    quotation.discount = quotation_data.discount
    quotation.final_amount = (
        quotation_data.total_amount
        - quotation_data.discount
    )
    quotation.valid_until = quotation_data.valid_until
    quotation.notes = quotation_data.notes

    db.commit()
    db.refresh(quotation)

    return quotation


def delete_quotation(
    db: Session,
    quotation_id: int,
):
    quotation = (
        db.query(Quotation)
        .filter(Quotation.id == quotation_id)
        .first()
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found."
        )

    if quotation.booking:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete quotation with existing booking."
        )

    db.delete(quotation)
    db.commit()

    return {
        "message": "Quotation deleted successfully."
    }