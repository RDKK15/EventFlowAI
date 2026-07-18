from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.permissions import require_owner
from app.auth.tenant import BusinessContext
from app.db.database import get_db
from app.models.business_user import BusinessUser
from app.schemas.user import BusinessUserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=list[BusinessUserResponse],
)
def read_users(
    db: Session = Depends(get_db),
    context: BusinessContext = Depends(require_owner),
):
    return (
        db.query(BusinessUser)
        .filter(
            BusinessUser.business_id == context.business_id,
        )
        .all()
    )