"""add business user membership architecture

Revision ID: 520fe4777840
Revises: e014e8ffab24
Create Date: 2026-07-12 19:28:17.740237

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "520fe4777840"
down_revision: Union[str, Sequence[str], None] = "e014e8ffab24"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create BusinessUser memberships and migrate legacy user ownership."""

    user_role_enum = postgresql.ENUM(
        "Owner",
        "Manager",
        "Staff",
        name="userrole",
        create_type=False,
    )

    op.create_table(
        "business_users",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "business_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "role",
            user_role_enum,
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["business_id"],
            ["businesses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "business_id",
            "user_id",
            name="uq_business_users_business_user",
        ),
    )

    op.create_index(
        "ix_business_users_id",
        "business_users",
        ["id"],
    )

    op.create_index(
        "ix_business_users_business_id",
        "business_users",
        ["business_id"],
    )

    op.create_index(
        "ix_business_users_user_id",
        "business_users",
        ["user_id"],
    )

    # Migrate only users that already belong to a valid business.
    op.execute(
        """
        INSERT INTO business_users (
            business_id,
            user_id,
            role,
            is_active,
            created_at,
            updated_at
        )
        SELECT
            u.business_id,
            u.id,
            u.role,
            u.is_active,
            u.created_at,
            u.updated_at
        FROM users AS u
        INNER JOIN businesses AS b
            ON b.id = u.business_id
        WHERE u.business_id IS NOT NULL
        """
    )

    # Verify every legacy user with a valid business was migrated.
    connection = op.get_bind()

    expected_memberships = connection.execute(
        sa.text(
            """
            SELECT COUNT(*)
            FROM users AS u
            INNER JOIN businesses AS b
                ON b.id = u.business_id
            WHERE u.business_id IS NOT NULL
            """
        )
    ).scalar_one()

    migrated_memberships = connection.execute(
        sa.text(
            """
            SELECT COUNT(*)
            FROM business_users
            """
        )
    ).scalar_one()

    if migrated_memberships != expected_memberships:
        raise RuntimeError(
            "BusinessUser migration verification failed: "
            f"expected {expected_memberships} memberships, "
            f"found {migrated_memberships}."
        )

    op.drop_constraint(
        "fk_users_business_id_businesses",
        "users",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_users_business_id",
        table_name="users",
    )

    op.drop_column(
        "users",
        "business_id",
    )

    op.drop_column(
        "users",
        "role",
    )


def downgrade() -> None:
    """Restore legacy single-business user ownership."""

    user_role_enum = postgresql.ENUM(
        "Owner",
        "Manager",
        "Staff",
        name="userrole",
        create_type=False,
    )

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role_enum,
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "business_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_users_business_id_businesses",
        "users",
        "businesses",
        ["business_id"],
        ["id"],
    )

    op.create_index(
        "ix_users_business_id",
        "users",
        ["business_id"],
    )

    op.execute(
        """
        UPDATE users AS u
        SET
            business_id = membership.business_id,
            role = membership.role
        FROM (
            SELECT DISTINCT ON (user_id)
                user_id,
                business_id,
                role
            FROM business_users
            ORDER BY user_id, id
        ) AS membership
        WHERE u.id = membership.user_id
        """
    )

    op.drop_index(
        "ix_business_users_user_id",
        table_name="business_users",
    )

    op.drop_index(
        "ix_business_users_business_id",
        table_name="business_users",
    )

    op.drop_index(
        "ix_business_users_id",
        table_name="business_users",
    )

    op.drop_table(
        "business_users",
    )