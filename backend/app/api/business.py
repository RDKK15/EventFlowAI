from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.business import BusinessCreate, BusinessResponse
from app.schemas.user import BusinessUserCreate, BusinessUserResponse
from app.services.business_service import (
    create_business,
    get_businesses,
    get_business_by_id,
)
from app.services.business_user_service import (
    create_business_user,
    get_users_by_business,
)

# ---------------------------------------------------------------------------
# DEVELOPMENT / BOOTSTRAP-ONLY ROUTER.
#
# {business_id} in the paths below is a URL path parameter, i.e. a plain
# client-controlled input. It is NOT a trusted tenant context and this
# router does not claim otherwise. There is currently no auth guard on
# any of these routes: right now, anyone who can reach this API can
# create a business or a user under any business_id, including one that
# isn't theirs. That is only acceptable because Phase 1 authentication
# has no concept of Business yet (users.business_id is nullable/
# transitional) -- there is no "theirs" to enforce yet.
#
# TODO (tenant isolation, later phase, not Phase 1):
# Once authentication is business-aware, business_id must be derived
# from the authenticated request, never from the URL, request body, an
# Excel import, or an AI system:
#
#     Authenticated user -> current_user -> current_user.business_id
#     -> all business-scoped queries
#
# At that point, POST /businesses/{business_id}/users (and any future
# business-scoped endpoint) should stop taking business_id from the
# path and instead scope to current_user.business_id, with a 403 if
# the path's business_id doesn't match.
# ---------------------------------------------------------------------------

router = APIRouter(
    prefix="/businesses",
    tags=["Businesses"],
)


@router.post(
    "/",
    response_model=BusinessResponse,
)
def create_business_endpoint(
    business: BusinessCreate,
    db: Session = Depends(get_db),
):
    return create_business(db, business)


@router.get(
    "/",
    response_model=list[BusinessResponse],
)
def list_businesses(
    db: Session = Depends(get_db),
):
    return get_businesses(db)


@router.get(
    "/{business_id}",
    response_model=BusinessResponse,
)
def read_business(
    business_id: int,
    db: Session = Depends(get_db),
):
    return get_business_by_id(db, business_id)


@router.post(
    "/{business_id}/users",
    response_model=BusinessUserResponse,
)
def create_user_for_business(
    business_id: int,
    user: BusinessUserCreate,
    db: Session = Depends(get_db),
):
    # DEV/BOOTSTRAP-ONLY: business_id is taken from the URL path, which is
    # client-controlled and not a trusted tenant context. See the router-
    # level comment above. Do not treat this endpoint as tenant-isolated.
    return create_business_user(db, business_id, user)


@router.get(
    "/{business_id}/users",
    response_model=list[BusinessUserResponse],
)
def list_users_for_business(
    business_id: int,
    db: Session = Depends(get_db),
):
    return get_users_by_business(db, business_id)
