from enum import Enum


class PaymentType(str, Enum):
    ADVANCE = "Advance"
    PARTIAL = "Partial"
    FINAL = "Final"


class PaymentMethod(str, Enum):
    CASH = "Cash"
    UPI = "UPI"
    BANK_TRANSFER = "Bank Transfer"