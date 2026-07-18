import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.tenant import BusinessContext
from app.db.database import Base
from app.enums.user import UserRole
from app.models.business import Business
from app.models.business_user import BusinessUser
from app.models.user import User
from app.schemas.business_configuration import (
    ServiceTypeCreate,
    ServiceTypeUpdate,
)
from app.services.business_configuration_service import (
    archive_service_type,
    create_service_type,
    get_service_type_for_business,
    list_service_types,
    update_service_type,
)


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
def tenant_contexts(db):
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

    context_one = BusinessContext(
        business=business_one,
        user=owner_one,
        membership=membership_one,
    )

    context_two = BusinessContext(
        business=business_two,
        user=owner_two,
        membership=membership_two,
    )

    return {
        "context_one": context_one,
        "context_two": context_two,
    }


def test_create_service_type(db, tenant_contexts):
    context_one = tenant_contexts["context_one"]

    service = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(
            name="Birthday Decoration",
            description="Balloon and theme decoration for birthdays.",
        ),
    )

    assert service.id is not None
    assert service.business_id == context_one.business_id
    assert service.name == "Birthday Decoration"
    assert service.is_active is True


def test_create_service_type_duplicate_name_rejected(db, tenant_contexts):
    context_one = tenant_contexts["context_one"]

    create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    with pytest.raises(HTTPException) as error:
        create_service_type(
            db,
            context_one,
            ServiceTypeCreate(name="Birthday Decoration"),
        )

    assert error.value.status_code == 409


def test_same_name_allowed_across_different_businesses(db, tenant_contexts):
    context_one = tenant_contexts["context_one"]
    context_two = tenant_contexts["context_two"]

    service_one = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    service_two = create_service_type(
        db,
        context_two,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    assert service_one.business_id != service_two.business_id
    assert service_one.name == service_two.name


def test_list_service_types_is_tenant_scoped(db, tenant_contexts):
    context_one = tenant_contexts["context_one"]
    context_two = tenant_contexts["context_two"]

    create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    create_service_type(
        db,
        context_two,
        ServiceTypeCreate(name="Wedding Decoration"),
    )

    business_one_services = list_service_types(db, context_one)
    business_two_services = list_service_types(db, context_two)

    assert [s.name for s in business_one_services] == [
        "Birthday Decoration"
    ]
    assert [s.name for s in business_two_services] == [
        "Wedding Decoration"
    ]


def test_get_service_type_for_owning_business(db, tenant_contexts):
    context_one = tenant_contexts["context_one"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    fetched = get_service_type_for_business(
        db,
        context_one,
        created.id,
    )

    assert fetched.id == created.id


def test_get_service_type_from_other_business_is_not_found(
    db,
    tenant_contexts,
):
    context_one = tenant_contexts["context_one"]
    context_two = tenant_contexts["context_two"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    with pytest.raises(HTTPException) as error:
        get_service_type_for_business(
            db,
            context_two,
            created.id,
        )

    assert error.value.status_code == 404


def test_update_service_type_name_and_description(db, tenant_contexts):
    context_one = tenant_contexts["context_one"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    updated = update_service_type(
        db,
        context_one,
        created.id,
        ServiceTypeUpdate(
            name="Birthday & Anniversary Decoration",
            description="Now covers anniversaries too.",
        ),
    )

    assert updated.name == "Birthday & Anniversary Decoration"
    assert updated.description == "Now covers anniversaries too."


def test_update_service_type_partial_fields_only(db, tenant_contexts):
    context_one = tenant_contexts["context_one"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(
            name="Birthday Decoration",
            description="Original description.",
        ),
    )

    updated = update_service_type(
        db,
        context_one,
        created.id,
        ServiceTypeUpdate(description="Updated description only."),
    )

    assert updated.name == "Birthday Decoration"
    assert updated.description == "Updated description only."


def test_update_service_type_duplicate_name_rejected(db, tenant_contexts):
    context_one = tenant_contexts["context_one"]

    create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Wedding Decoration"),
    )

    birthday = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    with pytest.raises(HTTPException) as error:
        update_service_type(
            db,
            context_one,
            birthday.id,
            ServiceTypeUpdate(name="Wedding Decoration"),
        )

    assert error.value.status_code == 409


def test_update_service_type_keep_own_name_is_allowed(db, tenant_contexts):
    context_one = tenant_contexts["context_one"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    updated = update_service_type(
        db,
        context_one,
        created.id,
        ServiceTypeUpdate(
            name="Birthday Decoration",
            description="Just adding a description.",
        ),
    )

    assert updated.name == "Birthday Decoration"
    assert updated.description == "Just adding a description."


def test_update_service_type_from_other_business_is_not_found(
    db,
    tenant_contexts,
):
    context_one = tenant_contexts["context_one"]
    context_two = tenant_contexts["context_two"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    with pytest.raises(HTTPException) as error:
        update_service_type(
            db,
            context_two,
            created.id,
            ServiceTypeUpdate(name="Hijacked Name"),
        )

    assert error.value.status_code == 404


def test_archive_service_type_soft_deletes(db, tenant_contexts):
    context_one = tenant_contexts["context_one"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    archived = archive_service_type(
        db,
        context_one,
        created.id,
    )

    assert archived.is_active is False


def test_archived_service_type_excluded_from_list(db, tenant_contexts):
    context_one = tenant_contexts["context_one"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    archive_service_type(
        db,
        context_one,
        created.id,
    )

    assert list_service_types(db, context_one) == []


def test_archived_service_type_still_gettable_by_id(db, tenant_contexts):
    """
    GET-by-id must keep resolving archived records so historical
    references (e.g. from a past Quotation) don't break, even
    though the service is hidden from active listings.
    """

    context_one = tenant_contexts["context_one"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    archive_service_type(
        db,
        context_one,
        created.id,
    )

    fetched = get_service_type_for_business(
        db,
        context_one,
        created.id,
        include_inactive=True,
    )

    assert fetched.id == created.id
    assert fetched.is_active is False


def test_archived_service_type_hidden_by_default_lookup(db, tenant_contexts):
    """
    Without include_inactive, an archived record is treated as not
    found - this is what Update/Archive rely on to prevent silently
    editing or double-archiving an archived record.
    """

    context_one = tenant_contexts["context_one"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    archive_service_type(
        db,
        context_one,
        created.id,
    )

    with pytest.raises(HTTPException) as error:
        get_service_type_for_business(
            db,
            context_one,
            created.id,
        )

    assert error.value.status_code == 404


def test_archived_service_type_from_other_business_not_found_even_with_include_inactive(
    db,
    tenant_contexts,
):
    """
    include_inactive relaxes the active-status filter only - it must
    never relax tenant isolation.
    """

    context_one = tenant_contexts["context_one"]
    context_two = tenant_contexts["context_two"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    archive_service_type(
        db,
        context_one,
        created.id,
    )

    with pytest.raises(HTTPException) as error:
        get_service_type_for_business(
            db,
            context_two,
            created.id,
            include_inactive=True,
        )

    assert error.value.status_code == 404


def test_archived_service_type_name_still_blocks_reuse(
    db,
    tenant_contexts,
):
    """
    The DB's UniqueConstraint(business_id, name) applies to all
    rows, active or archived, so archiving a service does not free
    up its name for a new service type in the same business.
    """

    context_one = tenant_contexts["context_one"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    archive_service_type(
        db,
        context_one,
        created.id,
    )

    with pytest.raises(HTTPException) as error:
        create_service_type(
            db,
            context_one,
            ServiceTypeCreate(name="Birthday Decoration"),
        )

    assert error.value.status_code == 409


def test_archive_service_type_from_other_business_is_not_found(
    db,
    tenant_contexts,
):
    context_one = tenant_contexts["context_one"]
    context_two = tenant_contexts["context_two"]

    created = create_service_type(
        db,
        context_one,
        ServiceTypeCreate(name="Birthday Decoration"),
    )

    with pytest.raises(HTTPException) as error:
        archive_service_type(
            db,
            context_two,
            created.id,
        )

    assert error.value.status_code == 404