from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.permissions import require_owner
from app.auth.tenant import BusinessContext
from app.db.database import get_db
from app.schemas.business_configuration import (
    ServiceTypeCreate,
    ServiceTypeResponse,
    ServiceTypeUpdate,
)
from app.services.business_configuration_service import (
    archive_service_type,
    create_service_type,
    get_service_type_for_business,
    list_service_types,
    update_service_type,
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


@router.get(
    "/service-types/{service_type_id}",
    response_model=ServiceTypeResponse,
)
def get_service_type_endpoint(
    service_type_id: int,
    db: Session = Depends(get_db),
    context: BusinessContext = Depends(require_owner),
):
    return get_service_type_for_business(
        db=db,
        context=context,
        service_type_id=service_type_id,
        include_inactive=True,
    )


@router.patch(
    "/service-types/{service_type_id}",
    response_model=ServiceTypeResponse,
)
def update_service_type_endpoint(
    service_type_id: int,
    data: ServiceTypeUpdate,
    db: Session = Depends(get_db),
    context: BusinessContext = Depends(require_owner),
):
    return update_service_type(
        db=db,
        context=context,
        service_type_id=service_type_id,
        data=data,
    )


@router.delete(
    "/service-types/{service_type_id}",
    response_model=ServiceTypeResponse,
)
def archive_service_type_endpoint(
    service_type_id: int,
    db: Session = Depends(get_db),
    context: BusinessContext = Depends(require_owner),
):
    return archive_service_type(
        db=db,
        context=context,
        service_type_id=service_type_id,
    )