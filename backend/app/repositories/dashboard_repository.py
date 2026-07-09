from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.customer import Customer
from app.models.enquiry import Enquiry
from app.models.payment import Payment
from app.models.quotation import Quotation


def get_total_customers(db: Session):
    return db.query(func.count(Customer.id)).scalar() or 0


def get_total_enquiries(db: Session):
    return db.query(func.count(Enquiry.id)).scalar() or 0


def get_total_quotations(db: Session):
    return db.query(func.count(Quotation.id)).scalar() or 0


def get_total_bookings(db: Session):
    return db.query(func.count(Booking.id)).scalar() or 0


def get_total_payments(db: Session):
    return db.query(func.count(Payment.id)).scalar() or 0


def get_total_revenue(db: Session):
    return db.query(func.sum(Payment.amount)).scalar() or 0


def get_pending_revenue(db: Session):
    total_revenue = get_total_revenue(db)

    total_quotation_amount = (
        db.query(func.sum(Quotation.final_amount))
        .scalar()
        or 0
    )

    return total_quotation_amount - total_revenue