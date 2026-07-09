from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.customer import Customer

from sqlalchemy import func
from app.models.payment import Payment
from app.models.quotation import Quotation
from app.models.enquiry import Enquiry


def get_total_customers(db: Session):
    return (
        db.query(func.count(Customer.id))
        .scalar()
        or 0
    )


def get_today_event_count(db: Session, today):
    return (
        db.query(Booking)
        .filter(
            func.date(Booking.event_start) == today
        )
        .count()
    )

def get_pending_payment_list(db: Session):

    rows = (
        db.query(
            Booking.booking_code,
            Customer.name,
            Enquiry.event_type,
            Quotation.final_amount,
            func.coalesce(func.sum(Payment.amount), 0).label("paid"),
        )
        .join(
            Quotation,
            Booking.quotation_id == Quotation.id,
        )
        .join(
            Enquiry,
            Quotation.enquiry_id == Enquiry.id,
        )
        .join(
            Customer,
            Enquiry.customer_id == Customer.id,
        )
        .outerjoin(
            Payment,
            Booking.id == Payment.booking_id,
        )
        .group_by(
            Booking.id,
            Booking.booking_code,
            Customer.name,
            Enquiry.event_type,
            Quotation.final_amount,
        )
        .all()
    )

    return rows