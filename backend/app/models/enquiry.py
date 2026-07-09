from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.database import Base


class Enquiry(Base):
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    enquiry_code = Column(String, unique=True, index=True)

    event_type = Column(String, nullable=False)

    preferred_date = Column(Date, nullable=False)

    flexible_date = Column(Boolean, default=False)

    venue_confirmed = Column(Boolean, default=False)

    venue_name = Column(String)

    venue_address = Column(String)

    guest_count = Column(Integer)

    budget_min = Column(Integer)

    budget_max = Column(Integer)

    decoration_theme = Column(String)

    lead_source = Column(String)

    stage = Column(String, default="New")

    notes = Column(String)

    customer = relationship(
        "Customer",
        back_populates="enquiries"
    )

    quotations = relationship(
        "Quotation",
        back_populates="enquiry"
    )
    