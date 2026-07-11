from enum import Enum


class SequenceType(str, Enum):
    """
    Known sequence types for BusinessSequence-based code generation.

    The database column (BusinessSequence.sequence_type) is a plain
    string, not a DB enum, so this list can grow as new domain models
    (Event, Quotation, Payment, ...) are introduced in later phases
    without requiring a schema migration. This enum exists purely for
    type safety in application code.
    """

    CUSTOMER = "CUSTOMER"
    EVENT = "EVENT"
    QUOTATION = "QUOTATION"
    PAYMENT = "PAYMENT"
