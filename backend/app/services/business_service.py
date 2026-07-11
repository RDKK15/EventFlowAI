from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.schemas.business import BusinessCreate


def create_business(
    db: Session,
    business_data: BusinessCreate,
) -> Business:

    if business_data.business_code:
        existing = (
            db.query(Business)
            .filter(Business.business_code == business_data.business_code)
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Business code already exists.",
            )

    new_business = Business(
        name=business_data.name,
        business_code=business_data.business_code,
    )

    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    return new_business


def get_businesses(db: Session):
    return db.query(Business).all()


def get_business_by_id(
    db: Session,
    business_id: int,
) -> Business:

    business = (
        db.query(Business)
        .filter(Business.id == business_id)
        .first()
    )

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found.",
        )

    return business
