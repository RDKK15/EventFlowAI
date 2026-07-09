from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_code = Column(String, unique=True, index=True)

    name = Column(String, nullable=False)

    phone = Column(String, unique=True, nullable=False)

    email = Column(String, unique=True, nullable=True)

    enquiries = relationship(
    "Enquiry",
    back_populates="customer"
)