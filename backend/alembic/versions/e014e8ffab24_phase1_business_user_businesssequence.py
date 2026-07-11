"""Phase 1: Business, BusinessSequence, User business_id/name/timestamps

Revision ID: e014e8ffab24
Revises: 7b37bd901e3f
Create Date: 2026-07-12 00:00:00.000000

DO NOT RUN `alembic upgrade head` UNTIL YOU HAVE INSPECTED YOUR DATABASE.

The migration this one is chained onto (7b37bd901e3f_initial_postgresql_schema)
has an EMPTY upgrade()/downgrade() -- it never actually created any tables.
That means Alembic's migration history does not reliably reflect what (if
anything) currently exists in your real Postgres database, and this
migration's ALTER TABLE users statements assume `users` already exists.

See backend/DATABASE_INSPECTION.md for:
  - the exact commands to run against your database first
  - safe, case-by-case migration plans depending on what those commands
    show (existing legacy schema / empty database / partially-applied
    Phase 1 schema / missing-or-inaccurate Alembic history)

Do not guess your database's state and do not run `alembic stamp head`
speculatively -- follow the case that actually matches what the
inspection commands return.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e014e8ffab24'
down_revision: Union[str, Sequence[str], None] = '7b37bd901e3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # --- businesses ---
    op.create_table(
        "businesses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("business_code", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_businesses_id", "businesses", ["id"])
    op.create_index("ix_businesses_business_code", "businesses", ["business_code"], unique=True)

    # --- users: add business_id / name / timestamps (all nullable / defaulted, non-destructive) ---
    op.add_column("users", sa.Column("business_id", sa.Integer(), nullable=True))
    op.add_column("users", sa.Column("name", sa.String(), nullable=True))
    op.add_column(
        "users",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.add_column(
        "users",
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_business_id", "users", ["business_id"])
    op.create_foreign_key(
        "fk_users_business_id_businesses",
        "users",
        "businesses",
        ["business_id"],
        ["id"],
    )

    # --- business_sequences ---
    op.create_table(
        "business_sequences",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("business_id", sa.Integer(), sa.ForeignKey("businesses.id"), nullable=False),
        sa.Column("sequence_type", sa.String(), nullable=False),
        sa.Column("current_value", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("business_id", "sequence_type", name="uq_business_sequence_business_id_sequence_type"),
    )
    op.create_index("ix_business_sequences_business_id", "business_sequences", ["business_id"])


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index("ix_business_sequences_business_id", table_name="business_sequences")
    op.drop_table("business_sequences")

    op.drop_constraint("fk_users_business_id_businesses", "users", type_="foreignkey")
    op.drop_index("ix_users_business_id", table_name="users")
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
    op.drop_column("users", "name")
    op.drop_column("users", "business_id")

    op.drop_index("ix_businesses_business_code", table_name="businesses")
    op.drop_table("businesses")
