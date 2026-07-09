from datetime import datetime

from pydantic import BaseModel


class TodayEvent(BaseModel):
    booking_code: str
    customer_name: str
    event_type: str
    venue_name: str
    event_start: datetime


class UpcomingEvent(BaseModel):
    booking_code: str
    customer_name: str
    event_type: str
    venue_name: str
    event_start: datetime


class PendingPayment(BaseModel):
    booking_code: str
    customer_name: str
    event_type: str
    total_amount: float
    paid_amount: float
    remaining_amount: float


class DashboardResponse(BaseModel):
    total_customers: int
    total_enquiries: int
    total_quotations: int
    total_bookings: int
    total_payments: int

    total_revenue: float
    pending_payments: float

    today_events: int
    upcoming_events: int

    monthly_revenue: float
    quotations_expiring: int

    today_event_list: list[TodayEvent]

    upcoming_event_list: list[UpcomingEvent]

    pending_payment_list: list[PendingPayment]