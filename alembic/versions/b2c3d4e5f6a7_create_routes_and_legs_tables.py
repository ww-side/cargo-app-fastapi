"""create routes and legs tables

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-02-07

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "routes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
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
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "legs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("route_id", sa.Integer(), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("origin_port", sa.String(), nullable=False),
        sa.Column("destination_port", sa.String(), nullable=False),
        sa.Column("vessel_id", sa.Integer(), nullable=True),
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
            "origin_port != destination_port",
            name="check_leg_different_ports",
        ),
        sa.ForeignKeyConstraint(
            ["route_id"],
            ["routes.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["vessel_id"],
            ["vessels.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_legs_route_id"), "legs", ["route_id"], unique=False)
    op.create_index(op.f("ix_legs_vessel_id"), "legs", ["vessel_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_legs_vessel_id"), table_name="legs")
    op.drop_index(op.f("ix_legs_route_id"), table_name="legs")
    op.drop_table("legs")
    op.drop_table("routes")
