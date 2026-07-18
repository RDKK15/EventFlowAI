from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.oauth2 import get_current_user
from app.db.database import get_db
from app.models.business import Business
from app.models.business_user import BusinessUser
from app.models.user import User


@dataclass
class BusinessContext:
    business: Business
    user: User
    membership: BusinessUser

    @property
    def business_id(self) -> int:
        return self.business.id


def get_business_context(
    x_business_id: int = Header(..., alias="X-Business-ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> BusinessContext:

    membership = (
        db.query(BusinessUser)
        .join(Business)
        .filter(
            BusinessUser.business_id == x_business_id,
            BusinessUser.user_id == current_user.id,
            BusinessUser.is_active.is_(True),
            Business.is_active.is_(True),
        )
        .first()
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this business.",
        )

    return BusinessContext(
        business=membership.business,
        user=current_user,
        membership=membership,
    )