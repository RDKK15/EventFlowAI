"""add business configuration core

Revision ID: 5537b88861d5
Revises: 520fe4777840
Create Date: 2026-07-12 20:04:01.181373

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "5537b88861d5"
down_revision: Union[str, Sequence[str], None] = "520fe4777840"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the business configuration core."""

    requirement_value_type = postgresql.ENUM(
        "Text",
        "LongText",
        "Integer",
        "Decimal",
        "Boolean",
        "Date",
        "DateTime",
        "SingleSelect",
        "MultiSelect",
        "Media",
        "ReferenceMedia",
        "CatalogReference",
        "StructuredDesign",
        name="requirementvaluetype",
    )

    requirement_collection_stage = postgresql.ENUM(
        "Enquiry",
        "Planning",
        "Execution",
        name="requirementcollectionstage",
    )

    requirement_value_type.create(
        op.get_bind(),
        checkfirst=True,
    )

    requirement_collection_stage.create(
        op.get_bind(),
        checkfirst=True,
    )

    requirement_value_type_column = postgresql.ENUM(
        "Text",
        "LongText",
        "Integer",
        "Decimal",
        "Boolean",
        "Date",
        "DateTime",
        "SingleSelect",
        "MultiSelect",
        "Media",
        "ReferenceMedia",
        "CatalogReference",
        "StructuredDesign",
        name="requirementvaluetype",
        create_type=False,
    )

    requirement_collection_stage_column = postgresql.ENUM(
        "Enquiry",
        "Planning",
        "Execution",
        name="requirementcollectionstage",
        create_type=False,
    )

    op.create_table(
        "service_types",
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
            "name",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["business_id"],
            ["businesses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "business_id",
            "name",
            name="uq_service_types_business_name",
        ),
    )

    op.create_index(
        "ix_service_types_business_id",
        "service_types",
        ["business_id"],
        unique=False,
    )

    op.create_index(
        "ix_service_types_id",
        "service_types",
        ["id"],
        unique=False,
    )

    op.create_table(
        "requirement_definitions",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "service_type_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "key",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "label",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "value_type",
            requirement_value_type_column,
            nullable=False,
        ),
        sa.Column(
            "unit",
            sa.String(),
            nullable=True,
        ),
        sa.Column(
            "is_required",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "ask_customer",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "collection_stage",
            requirement_collection_stage_column,
            nullable=False,
        ),
        sa.Column(
            "display_order",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "ai_hint",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["service_type_id"],
            ["service_types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "service_type_id",
            "key",
            name="uq_requirement_definitions_service_key",
        ),
    )

    op.create_index(
        "ix_requirement_definitions_id",
        "requirement_definitions",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_requirement_definitions_service_type_id",
        "requirement_definitions",
        ["service_type_id"],
        unique=False,
    )

    op.create_table(
        "requirement_options",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "requirement_definition_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "value",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "label",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "display_order",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["requirement_definition_id"],
            ["requirement_definitions.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "requirement_definition_id",
            "value",
            name="uq_requirement_options_definition_value",
        ),
    )

    op.create_index(
        "ix_requirement_options_id",
        "requirement_options",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_requirement_options_requirement_definition_id",
        "requirement_options",
        ["requirement_definition_id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove the business configuration core."""

    op.drop_index(
        "ix_requirement_options_requirement_definition_id",
        table_name="requirement_options",
    )

    op.drop_index(
        "ix_requirement_options_id",
        table_name="requirement_options",
    )

    op.drop_table(
        "requirement_options",
    )

    op.drop_index(
        "ix_requirement_definitions_service_type_id",
        table_name="requirement_definitions",
    )

    op.drop_index(
        "ix_requirement_definitions_id",
        table_name="requirement_definitions",
    )

    op.drop_table(
        "requirement_definitions",
    )

    op.drop_index(
        "ix_service_types_id",
        table_name="service_types",
    )

    op.drop_index(
        "ix_service_types_business_id",
        table_name="service_types",
    )

    op.drop_table(
        "service_types",
    )

    requirement_collection_stage = postgresql.ENUM(
        "Enquiry",
        "Planning",
        "Execution",
        name="requirementcollectionstage",
    )

    requirement_value_type = postgresql.ENUM(
        "Text",
        "LongText",
        "Integer",
        "Decimal",
        "Boolean",
        "Date",
        "DateTime",
        "SingleSelect",
        "MultiSelect",
        "Media",
        "ReferenceMedia",
        "CatalogReference",
        "StructuredDesign",
        name="requirementvaluetype",
    )

    requirement_collection_stage.drop(
        op.get_bind(),
        checkfirst=True,
    )

    requirement_value_type.drop(
        op.get_bind(),
        checkfirst=True,
    )