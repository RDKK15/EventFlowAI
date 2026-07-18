from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.tenant import BusinessContext
from app.models.service_type import ServiceType
from app.schemas.business_configuration import (
    ServiceTypeCreate,
    ServiceTypeUpdate,
)


def get_service_type_for_business(
    db: Session,
    context: BusinessContext,
    service_type_id: int,
    include_inactive: bool = False,
) -> ServiceType:
    """
    Return a ServiceType that belongs to the current business.

    Never expose another business's configuration.

    By default only active services are returned, since editing
    or re-archiving an already-archived service is not allowed
    without an explicit restore step. Pass include_inactive=True
    for read-only lookups (e.g. resolving a historical reference
    from a Quotation or Enquiry), where an archived service must
    still be viewable even though it's hidden from active lists.
    """

    filters = [
        ServiceType.id == service_type_id,
        ServiceType.business_id == context.business_id,
    ]

    if not include_inactive:
        filters.append(ServiceType.is_active.is_(True))

    service_type = db.query(ServiceType).filter(*filters).first()

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
    exclude_service_type_id: int | None = None,
) -> None:
    """
    Prevent duplicate service names inside one business.

    This mirrors the database's UniqueConstraint on
    (business_id, name), which applies across ALL rows regardless
    of is_active. Archived service names are therefore not
    available for reuse in this schema; loosening that would
    require a migration to a partial unique index and is out of
    scope for this feature.

    TODO(ADR-001): If the product later requires archived
    ServiceType names to be reusable (e.g. a business re-adds a
    service it previously discontinued), replace the current
    UniqueConstraint("business_id", "name") with a partial/filtered
    unique index scoped to is_active = true. That requires a new
    Alembic migration and should go through the ADR process first
    (see docs/adr/ADR-001-service-type-archived-name-reuse.md) -
    do not change this check without that migration landing first.

    exclude_service_type_id lets an update keep the service type's
    own current name without conflicting with itself.
    """

    query = db.query(ServiceType).filter(
        ServiceType.business_id == context.business_id,
        ServiceType.name == name,
    )

    if exclude_service_type_id is not None:
        query = query.filter(
            ServiceType.id != exclude_service_type_id,
        )

    existing = query.first()

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


def update_service_type(
    db: Session,
    context: BusinessContext,
    service_type_id: int,
    data: ServiceTypeUpdate,
) -> ServiceType:
    """
    Update a service belonging to the current business.

    Only fields explicitly provided are changed.
    """

    service = get_service_type_for_business(
        db,
        context,
        service_type_id,
    )

    if data.name is not None:
        ensure_unique_service_name(
            db,
            context,
            data.name,
            exclude_service_type_id=service.id,
        )

        service.name = data.name.strip()

    if data.description is not None:
        service.description = data.description

    db.commit()

    db.refresh(service)

    return service


def archive_service_type(
    db: Session,
    context: BusinessContext,
    service_type_id: int,
) -> ServiceType:
    """
    Archive (soft delete) a service belonging to the current business.

    Business history is preserved; the service is simply hidden
    from future listings and lookups.
    """

    service = get_service_type_for_business(
        db,
        context,
        service_type_id,
    )

    service.is_active = False

    db.commit()

    db.refresh(service)

    return service