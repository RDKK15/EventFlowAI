# Centralized model registration.
#
# SQLAlchemy's declarative mapper configuration needs every mapped class
# referenced by a string-based relationship() (e.g. relationship("Business"))
# to have its module actually imported (executed) before that relationship
# is first used -- not just the module of the class doing the referencing.
#
# This project's models form one connected relationship graph:
#   Customer <-> Enquiry <-> Quotation <-> Booking <-> Payment
#   User <-> Business <-> BusinessSequence
#
# Previously, the only place all of them were imported together was
# app/main.py. Anything that imported a single model (or a service that
# imports a single model, e.g. business_sequence_service importing only
# BusinessSequence) without going through app.main -- a standalone script,
# a bare Alembic run, a unit test -- could hit
# `InvalidRequestError: expression 'Business' failed to locate a name`
# because Business/User had never actually been imported in that process.
#
# Importing this package (app.models) guarantees every mapped class is
# registered, regardless of which one was needed. app/db/database.py
# imports this package once, after Base is defined, so that guarantee
# holds for every code path that touches the database (app.main,
# alembic/env.py, services, and standalone scripts alike).

from app.models.customer import Customer
from app.models.enquiry import Enquiry
from app.models.quotation import Quotation
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.user import User
from app.models.business import Business
from app.models.business_sequence import BusinessSequence

__all__ = [
    "Customer",
    "Enquiry",
    "Quotation",
    "Booking",
    "Payment",
    "User",
    "Business",
    "BusinessSequence",
]
