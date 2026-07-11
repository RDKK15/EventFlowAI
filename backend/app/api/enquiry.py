from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.db.database import get_db

from app.schemas.enquiry import (
    EnquiryCreate,
    EnquiryUpdate,
    EnquiryResponse,
)

from app.services.enquiry_service import (
    create_enquiry,
    get_enquiries,
    get_enquiry_by_id,
    update_enquiry,
    delete_enquiry,
)

router = APIRouter(
    prefix="/enquiries",
    tags=["Enquiries"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=EnquiryResponse)
def add_enquiry(
    enquiry: EnquiryCreate,
    db: Session = Depends(get_db),
):
    return create_enquiry(db, enquiry)


@router.get("/", response_model=list[EnquiryResponse])
def read_enquiries(
    event_type: str | None = None,
    venue_name: str | None = None,
    budget_min: float | None = None,
    budget_max: float | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    return get_enquiries(
        db=db,
        event_type=event_type,
        venue_name=venue_name,
        budget_min=budget_min,
        budget_max=budget_max,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
    )


@router.get("/{enquiry_id}", response_model=EnquiryResponse)
def read_enquiry(
    enquiry_id: int,
    db: Session = Depends(get_db),
):
    return get_enquiry_by_id(
        db,
        enquiry_id,
    )


@router.put("/{enquiry_id}", response_model=EnquiryResponse)
def edit_enquiry(
    enquiry_id: int,
    enquiry: EnquiryUpdate,
    db: Session = Depends(get_db),
):
    return update_enquiry(
        db,
        enquiry_id,
        enquiry,
    )


@router.delete("/{enquiry_id}")
def remove_enquiry(
    enquiry_id: int,
    db: Session = Depends(get_db),
):
    return delete_enquiry(
        db,
        enquiry_id,
    )