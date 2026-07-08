from sqlalchemy.orm import Session

from app.models.enquiry import Enquiry
from app.schemas.enquiry import EnquiryCreate


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

    return new_enquiry


def get_enquiries(db: Session):
    return db.query(Enquiry).all()