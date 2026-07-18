from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.tenant import BusinessContext
from app.models.service_type import ServiceType
from app.schemas.business_configuration import ServiceTypeCreate


def get_service_type_for_business(
    db: Session,
    context: BusinessContext,
    service_type_id: int,
) -> ServiceType:
    """
    Return a ServiceType that belongs to the current business.

    Never expose another business's configuration.
    """

    service_type = (
        db.query(ServiceType)
        .filter(
            ServiceType.id == service_type_id,
            ServiceType.business_id == context.business_id,
            ServiceType.is_active.is_(True),
        )
        .first()
    )

    if service_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service type not found.",
        )

    return service_type


def ensure_unique_service_name(
    db: Session,
    context: BusinessContext,
    name: str,
) -> None:
    """
    Prevent duplicate service names inside one business.
    """

    existing = (
        db.query(ServiceType)
        .filter(
            ServiceType.business_id == context.business_id,
            ServiceType.name == name,
            ServiceType.is_active.is_(True),
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A service with this name already exists.",
        )


def create_service_type(
    db: Session,
    context: BusinessContext,
    data: ServiceTypeCreate,
) -> ServiceType:
    """
    Create a new service for the current business.
    """

    ensure_unique_service_name(
        db,
        context,
        data.name,
    )

    service = ServiceType(
        business_id=context.business_id,
        name=data.name.strip(),
        description=data.description,
        is_active=True,
    )

    db.add(service)

    db.commit()

    db.refresh(service)

    return service


def list_service_types(
    db: Session,
    context: BusinessContext,
) -> list[ServiceType]:
    """
    List all active services for the current business.
    """

    return (
        db.query(ServiceType)
        .filter(
            ServiceType.business_id == context.business_id,
            ServiceType.is_active.is_(True),
        )
        .order_by(ServiceType.name.asc())
        .all()
    )