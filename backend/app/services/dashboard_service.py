from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.customer import Customer
from app.models.enquiry import Enquiry
from app.models.payment import Payment
from app.models.quotation import Quotation

from app.repositories.dashboard_repository import (
    get_total_customers,
    get_total_enquiries,
    get_total_quotations,
    get_total_bookings,
    get_total_payments,
    get_total_revenue,
    get_pending_revenue,
    
)

from app.schemas.dashboard import (
    DashboardResponse,
    TodayEvent,
    UpcomingEvent, PendingPayment  
)


def get_dashboard(db: Session):

    total_customers = get_total_customers(db)

    total_enquiries = get_total_enquiries(db)

    total_quotations = get_total_quotations(db)

    total_bookings = get_total_bookings(db)

    total_payments = get_total_payments(db)

    total_revenue = get_total_revenue(db)

    pending_payments = get_pending_revenue(db)

    today = date.today()

    # Today's Events Count
    today_events = (
    db.query(Booking)
    .filter(
        func.date(Booking.event_start) == today
    )
    .count()
)


    # Today's Event List
    today_event_rows = (
        db.query(
            Booking.booking_code,
            Customer.name,
            Enquiry.event_type,
            Booking.venue_name,
            Booking.event_start,
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
        .filter(
            func.date(Booking.event_start) == today
        )
        .all()
    )

    next_week = today + timedelta(days=7)

    upcoming_events = (
        db.query(Booking)
        .filter(
            func.date(Booking.event_start) > today,
            func.date(Booking.event_start) <= next_week,
        )
        .count()
    )
    upcoming_event_rows = (
    db.query(
        Booking.booking_code,
        Customer.name,
        Enquiry.event_type,
        Booking.venue_name,
        Booking.event_start,
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
    .filter(
        func.date(Booking.event_start) > today,
        func.date(Booking.event_start) <= next_week,
    )
    .order_by(Booking.event_start)
    .all()
)

    monthly_revenue = (
        db.query(func.sum(Payment.amount))
        .filter(
            func.strftime(
                "%Y-%m",
                Payment.payment_date,
            )
            == today.strftime("%Y-%m")
        )
        .scalar()
        or 0
    )

    three_days = today + timedelta(days=3)

    quotations_expiring = (
        db.query(Quotation)
        .filter(
            Quotation.valid_until >= today,
            Quotation.valid_until <= three_days,
        )
        .count()
    )

    return DashboardResponse(
    total_customers=total_customers,
    total_enquiries=total_enquiries,
    total_quotations=total_quotations,
    total_bookings=total_bookings,
    total_payments=total_payments,
    total_revenue=total_revenue,
    pending_payments=pending_payments,
    today_events=today_events,
    upcoming_events=upcoming_events,
    monthly_revenue=monthly_revenue,
    quotations_expiring=quotations_expiring,

    today_event_list=[
        TodayEvent(
            booking_code=row.booking_code,
            customer_name=row.name,
            event_type=row.event_type,
            venue_name=row.venue_name,
            event_start=row.event_start,
        )
        for row in today_event_rows
    ],

    upcoming_event_list=[
        UpcomingEvent(
            booking_code=row.booking_code,
            customer_name=row.name,
            event_type=row.event_type,
            venue_name=row.venue_name,
            event_start=row.event_start,
        )
        for row in upcoming_event_rows
    ],
)
