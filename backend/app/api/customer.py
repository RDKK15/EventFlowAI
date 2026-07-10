from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.permissions import require_owner
from app.models.user import User

from app.db.database import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)
from app.services.customer_service import (
    create_customer,
    get_customers,
    get_customer_by_id,
    update_customer,
    delete_customer,
)

from app.auth.oauth2 import get_current_user
from app.models.user import User

from fastapi import Depends
from app.auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    dependencies=[Depends(get_current_user)],
)

sort_by: str = "id",
order: str = "asc",


@router.post("/", response_model=CustomerResponse)
def add_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return create_customer(db, customer)


@router.get("/", response_model=list[CustomerResponse])
def read_customers(
    name: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    return get_customers(
        db,
        name=name,
        phone=phone,
        email=email,
        page=page,
        limit=limit,
        sort_by=sort_by,
        order=order,
    )

@router.put("/{customer_id}", response_model=CustomerResponse)
def edit_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
):
    return update_customer(
        db,
        customer_id,
        customer,
    )

@router.delete("/{customer_id}")
def remove_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner),
):
    return delete_customer(db, customer_id)