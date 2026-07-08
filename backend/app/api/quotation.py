from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.quotation import (
    QuotationCreate,
    QuotationResponse,
)
from app.services.quotation_service import (
    create_quotation,
    get_quotations,
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