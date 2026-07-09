from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate 
from app.utils.code_generator import generate_code



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

    # Create customer first
    new_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        email=customer.email
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    # Generate friendly customer code
    new_customer.customer_code = generate_code("C", new_customer.id)

    db.commit()
    db.refresh(new_customer)

    return new_customer


def get_customers(db: Session):
    return db.query(Customer).all()

def get_customer_by_id(db: Session, customer_id: int):

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    return customer


def update_customer(
    db: Session,
    customer_id: int,
    customer_data: CustomerUpdate,
):

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    # Check duplicate phone
    existing_phone = (
        db.query(Customer)
        .filter(
            Customer.phone == customer_data.phone,
            Customer.id != customer_id,
        )
        .first()
    )

    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists."
        )

    # Check duplicate email
    if customer_data.email:
        existing_email = (
            db.query(Customer)
            .filter(
                Customer.email == customer_data.email,
                Customer.id != customer_id,
            )
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists."
            )

    customer.name = customer_data.name
    customer.phone = customer_data.phone
    customer.email = customer_data.email

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(
    db: Session,
    customer_id: int,
):

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    if customer.enquiries:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete customer with existing enquiries."
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully."
    }