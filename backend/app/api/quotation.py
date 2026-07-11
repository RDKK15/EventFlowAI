from fastapi import APIRouter, Depends
from app.auth.oauth2 import get_current_user
from sqlalchemy.orm import Session

from datetime import date

from app.db.database import get_db
from app.schemas.quotation import (
    QuotationCreate,
    QuotationUpdate,
    QuotationResponse,
)
from app.services.quotation_service import (
    create_quotation,
    get_quotations,
    get_quotation_by_id,
    update_quotation,
    delete_quotation,
)


router = APIRouter(
    prefix="/quotations",
    tags=["Quotations"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=QuotationResponse)
def add_quotation(
    quotation: QuotationCreate,
    db: Session = Depends(get_db),
):
    return create_quotation(db, quotation)


@router.get("/", response_model=list[QuotationResponse])
def read_quotations(
    quotation_code: str | None = None,
    status: str | None = None,
    amount_min: int | None = None,
    amount_max: int | None = None,
    valid_until_from: date | None = None,
    valid_until_to: date | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    return get_quotations(
        db=db,
        quotation_code=quotation_code,
        status=status,
        amount_min=amount_min,
        amount_max=amount_max,
        valid_until_from=valid_until_from,
        valid_until_to=valid_until_to,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
    )


@router.get("/{quotation_id}", response_model=QuotationResponse)
def read_quotation(
    quotation_id: int,
    db: Session = Depends(get_db),
):
    return get_quotation_by_id(
        db,
        quotation_id,
    )


@router.put("/{quotation_id}", response_model=QuotationResponse)
def edit_quotation(
    quotation_id: int,
    quotation: QuotationUpdate,
    db: Session = Depends(get_db),
):
    return update_quotation(
        db,
        quotation_id,
        quotation,
    )


@router.delete("/{quotation_id}")
def remove_quotation(
    quotation_id: int,
    db: Session = Depends(get_db),
):
    return delete_quotation(
        db,
        quotation_id,
    )