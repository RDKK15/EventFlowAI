from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.enquiry import Enquiry
from app.models.quotation import Quotation
from app.schemas.quotation import QuotationCreate
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