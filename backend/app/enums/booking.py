from enum import Enum


class BookingStatus(str, Enum):
    PROPOSAL = "Proposal"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"