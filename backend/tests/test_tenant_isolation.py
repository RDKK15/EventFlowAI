import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.tenant import get_business_context
from app.db.database import Base
from app.enums.user import UserRole
from app.models.business import Business
from app.models.business_user import BusinessUser
from app.models.user import User


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def tenant_data(db):
    business_one = Business(
        name="Business One",
        business_code="BUS1",
        is_active=True,
    )

    business_two = Business(
        name="Business Two",
        business_code="BUS2",
        is_active=True,
    )

    owner_one = User(
        name="Owner One",
        username="owner_one",
        email="owner1@test.com",
        hashed_password="test",
        is_active=True,
    )

    owner_two = User(
        name="Owner Two",
        username="owner_two",
        email="owner2@test.com",
        hashed_password="test",
        is_active=True,
    )

    db.add_all(
        [
            business_one,
            business_two,
            owner_one,
            owner_two,
        ]
    )

    db.flush()

    membership_one = BusinessUser(
        business_id=business_one.id,
        user_id=owner_one.id,
        role=UserRole.OWNER,
        is_active=True,
    )

    membership_two = BusinessUser(
        business_id=business_two.id,
        user_id=owner_two.id,
        role=UserRole.OWNER,
        is_active=True,
    )

    db.add_all(
        [
            membership_one,
            membership_two,
        ]
    )

    db.commit()

    return {
        "business_one": business_one,
        "business_two": business_two,
        "owner_one": owner_one,
        "owner_two": owner_two,
    }


def test_owner_one_can_access_business_one(
    db,
    tenant_data,
):
    context = get_business_context(
        x_business_id=tenant_data["business_one"].id,
        current_user=tenant_data["owner_one"],
        db=db,
    )

    assert context.business_id == tenant_data["business_one"].id
    assert context.user.id == tenant_data["owner_one"].id


def test_owner_one_cannot_access_business_two(
    db,
    tenant_data,
):
    with pytest.raises(HTTPException) as error:
        get_business_context(
            x_business_id=tenant_data["business_two"].id,
            current_user=tenant_data["owner_one"],
            db=db,
        )

    assert error.value.status_code == 403
    assert (
        error.value.detail
        == "You do not have access to this business."
    )


def test_owner_two_can_access_business_two(
    db,
    tenant_data,
):
    context = get_business_context(
        x_business_id=tenant_data["business_two"].id,
        current_user=tenant_data["owner_two"],
        db=db,
    )

    assert context.business_id == tenant_data["business_two"].id
    assert context.user.id == tenant_data["owner_two"].id


def test_owner_two_cannot_access_business_one(
    db,
    tenant_data,
):
    with pytest.raises(HTTPException) as error:
        get_business_context(
            x_business_id=tenant_data["business_one"].id,
            current_user=tenant_data["owner_two"],
            db=db,
        )

    assert error.value.status_code == 403
    assert (
        error.value.detail
        == "You do not have access to this business."
    )