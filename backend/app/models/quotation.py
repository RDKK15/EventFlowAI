from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.database import Base


class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)

    quotation_code = Column(String, unique=True, index=True)

    enquiry_id = Column(Integer, ForeignKey("enquiries.id"))

    total_amount = Column(Integer, nullable=False)

    discount = Column(Integer, default=0)

    final_amount = Column(Integer, nullable=False)

    valid_until = Column(Date)

    status = Column(String, default="Draft")

    notes = Column(String)

    enquiry = relationship(
        "Enquiry",
        back_populates="quotations"
)
    booking = relationship(
        "Booking",
        back_populates="quotation",
        uselist=False
)