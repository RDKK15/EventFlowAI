from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
)


@router.post("/", response_model=QuotationResponse)
def add_quotation(
    quotation: QuotationCreate,
    db: Session = Depends(get_db),
):
    return create_quotation(db, quotation)


@router.get("/", response_model=list[QuotationResponse])
def read_quotations(
    db: Session = Depends(get_db),
):
    return get_quotations(db)


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