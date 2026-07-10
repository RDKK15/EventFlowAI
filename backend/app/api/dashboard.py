from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import get_dashboard

from fastapi import APIRouter, Depends
from app.auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=DashboardResponse)
def read_dashboard(
    db: Session = Depends(get_db),
):
    return get_dashboard(db)