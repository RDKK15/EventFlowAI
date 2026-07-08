from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.enquiry import EnquiryCreate, EnquiryResponse
from app.services.enquiry_service import (
    create_enquiry,
    get_enquiries,
)

router = APIRouter(
    prefix="/enquiries",
    tags=["Enquiries"],
)


@router.post("/", response_model=EnquiryResponse)
def add_enquiry(
    enquiry: EnquiryCreate,
    db: Session = Depends(get_db),
):
    return create_enquiry(db, enquiry)


@router.get("/", response_model=list[EnquiryResponse])
def read_enquiries(
    db: Session = Depends(get_db),
):
    return get_enquiries(db)