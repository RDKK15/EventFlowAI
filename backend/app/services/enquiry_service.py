from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.enquiry import Enquiry
from app.schemas.enquiry import EnquiryCreate, EnquiryUpdate
from app.utils.code_generator import generate_code


def create_enquiry(db: Session, enquiry: EnquiryCreate):

    new_enquiry = Enquiry(
        customer_id=enquiry.customer_id,
        event_type=enquiry.event_type,
        preferred_date=enquiry.preferred_date,
        flexible_date=enquiry.flexible_date,
        venue_confirmed=enquiry.venue_confirmed,
        venue_name=enquiry.venue_name,
        venue_address=enquiry.venue_address,
        guest_count=enquiry.guest_count,
        budget_min=enquiry.budget_min,
        budget_max=enquiry.budget_max,
        decoration_theme=enquiry.decoration_theme,
        lead_source=enquiry.lead_source,
        notes=enquiry.notes,
    )

    db.add(new_enquiry)
    db.commit()
    db.refresh(new_enquiry)

    # Generate friendly enquiry code
    new_enquiry.enquiry_code = generate_code(
        "E",
        new_enquiry.id
    )

    db.commit()
    db.refresh(new_enquiry)

    return new_enquiry


def get_enquiries(db: Session):
    return db.query(Enquiry).all()


def get_enquiry_by_id(
    db: Session,
    enquiry_id: int,
):
    enquiry = (
        db.query(Enquiry)
        .filter(Enquiry.id == enquiry_id)
        .first()
    )

    if not enquiry:
        raise HTTPException(
            status_code=404,
            detail="Enquiry not found."
        )

    return enquiry


def update_enquiry(
    db: Session,
    enquiry_id: int,
    enquiry_data: EnquiryUpdate,
):
    enquiry = (
        db.query(Enquiry)
        .filter(Enquiry.id == enquiry_id)
        .first()
    )

    if not enquiry:
        raise HTTPException(
            status_code=404,
            detail="Enquiry not found."
        )

    enquiry.customer_id = enquiry_data.customer_id
    enquiry.event_type = enquiry_data.event_type
    enquiry.preferred_date = enquiry_data.preferred_date
    enquiry.flexible_date = enquiry_data.flexible_date
    enquiry.venue_confirmed = enquiry_data.venue_confirmed
    enquiry.venue_name = enquiry_data.venue_name
    enquiry.venue_address = enquiry_data.venue_address
    enquiry.guest_count = enquiry_data.guest_count
    enquiry.budget_min = enquiry_data.budget_min
    enquiry.budget_max = enquiry_data.budget_max
    enquiry.decoration_theme = enquiry_data.decoration_theme
    enquiry.lead_source = enquiry_data.lead_source
    enquiry.notes = enquiry_data.notes

    db.commit()
    db.refresh(enquiry)

    return enquiry


def delete_enquiry(
    db: Session,
    enquiry_id: int,
):
    enquiry = (
        db.query(Enquiry)
        .filter(Enquiry.id == enquiry_id)
        .first()
    )

    if not enquiry:
        raise HTTPException(
            status_code=404,
            detail="Enquiry not found."
        )

    if enquiry.quotations:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete enquiry with existing quotations."
        )

    db.delete(enquiry)
    db.commit()

    return {
        "message": "Enquiry deleted successfully."
    }