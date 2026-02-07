"""create bookings table

Revision ID: a1b2c3d4e5f6
Revises: c2e2eafb2951
Create Date: 2026-02-07

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "c2e2eafb2951"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # btree_gist extension required for exclusion constraint with integer (vessel_id)
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("vessel_id", sa.Integer(), nullable=False),
        sa.Column("reserved_capacity", sa.Float(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("port_name", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "reserved_capacity > 0",
            name="check_reserved_capacity_positive",
        ),
        sa.CheckConstraint(
            "end_time > start_time",
            name="check_valid_time_range",
        ),
        sa.ForeignKeyConstraint(
            ["vessel_id"],
            ["vessels.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_bookings_vessel_id"),
        "bookings",
        ["vessel_id"],
        unique=False,
    )

    # Exclusion constraint: vessel cannot have overlapping time ranges
    op.execute(
        """
        ALTER TABLE bookings
        ADD CONSTRAINT excl_vessel_no_overlapping_bookings
        EXCLUDE USING gist (
            vessel_id WITH =,
            tstzrange(start_time, end_time) WITH &&
        )
        """
    )


def downgrade() -> None:
    op.drop_constraint(
        "excl_vessel_no_overlapping_bookings",
        "bookings",
        type_="exclusion",
    )
    op.drop_index(op.f("ix_bookings_vessel_id"), table_name="bookings")
    op.drop_table("bookings")
    # Note: we don't DROP EXTENSION btree_gist as it may be used elsewhere
