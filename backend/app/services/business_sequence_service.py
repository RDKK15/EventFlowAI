from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from app.models.business_sequence import BusinessSequence


def get_next_sequence_value(
    db: Session,
    business_id: int,
    sequence_type: str,
) -> int:
    """
    Atomically find-or-create-and-increment the BusinessSequence row for
    (business_id, sequence_type), returning the new current_value.

    Implementation: a single PostgreSQL INSERT ... ON CONFLICT (business_id,
    sequence_type) DO UPDATE SET current_value = current_value + 1 RETURNING
    current_value.

    Why this replaces the earlier SELECT ... FOR UPDATE + catch-IntegrityError
    approach: that approach called db.rollback() on a race, which rolls back
    the entire Session's transaction -- not just this statement. Since this
    function is meant to be reused inside a larger unit of work (e.g. while
    a caller is also building a Customer/Event/Quotation row in the same
    transaction before a single commit), rolling back here could silently
    discard that caller's pending, uncommitted work. A single atomic
    upsert statement has no failure branch that requires a rollback: on a
    race, PostgreSQL's own row-level conflict resolution handles it, not us.

    This function only flushes (via the statement's autoflush-safe
    execution), never commits. Committing remains the caller's
    responsibility, same as before.

    PostgreSQL-specific by design: this uses
    sqlalchemy.dialects.postgresql.insert, which only compiles against the
    postgresql dialect. Production is PostgreSQL, per the locked
    architecture, so no SQLite fallback is included here -- see the
    docstring note in the test suite for how tests around this function
    are (and aren't) run.
    """

    stmt = pg_insert(BusinessSequence).values(
        business_id=business_id,
        sequence_type=sequence_type,
        current_value=1,
    )

    stmt = stmt.on_conflict_do_update(
        index_elements=[
            BusinessSequence.business_id,
            BusinessSequence.sequence_type,
        ],
        set_={
            "current_value": BusinessSequence.current_value + 1,
        },
    ).returning(BusinessSequence.current_value)

    result = db.execute(stmt)
    next_value = result.scalar_one()

    return next_value


def generate_business_code(
    db: Session,
    business_id: int,
    sequence_type: str,
    prefix: str,
) -> str:
    """
    Reusable code generator for future Customer/Event/Quotation/Payment
    services. Not wired into any existing model in Phase 1.

    Example: generate_business_code(db, business_id=1, sequence_type="EVENT", prefix="EVT")
    -> "EVT-0001"
    """

    next_value = get_next_sequence_value(
        db,
        business_id,
        sequence_type,
    )

    return f"{prefix}-{next_value:04d}"
