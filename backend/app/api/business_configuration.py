from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.permissions import require_owner
from app.auth.tenant import BusinessContext
from app.db.database import get_db
from app.schemas.business_configuration import (
    ServiceTypeCreate,
    ServiceTypeResponse,
)
from app.services.business_configuration_service import (
    create_service_type,
    list_service_types,
)

router = APIRouter(
    prefix="/business-configuration",
    tags=["Business Configuration"],
)


@router.post(
    "/service-types",
    response_model=ServiceTypeResponse,
    status_code=201,
)
def create_service_type_endpoint(
    data: ServiceTypeCreate,
    db: Session = Depends(get_db),
    context: BusinessContext = Depends(require_owner),
):
    return create_service_type(
        db=db,
        context=context,
        data=data,
    )


@router.get(
    "/service-types",
    response_model=list[ServiceTypeResponse],
)
def list_service_types_endpoint(
    db: Session = Depends(get_db),
    context: BusinessContext = Depends(require_owner),
):
    return list_service_types(
        db=db,
        context=context,
    )