from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


def create_customer(db: Session, customer: CustomerCreate):

    existing_phone = (
        db.query(Customer)
        .filter(Customer.phone == customer.phone)
        .first()
    )

    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists."
        )

    if customer.email:
        existing_email = (
            db.query(Customer)
            .filter(Customer.email == customer.email)
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists."
            )

    new_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        email=customer.email
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


def get_customers(db: Session):
    return db.query(Customer).all()