"""create shipments and audit trigger

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-02-07

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, Sequence[str], None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "shipments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("booking_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "CONFIRMED",
                "SHIPPED",
                "IN_TRANSIT",
                "DELIVERED",
                "CANCELLED",
                name="shipmentstatus",
            ),
            nullable=False,
        ),
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
        sa.ForeignKeyConstraint(
            ["booking_id"],
            ["bookings.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_shipments_booking_id"),
        "shipments",
        ["booking_id"],
        unique=False,
    )

    op.create_table(
        "shipment_audit",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("shipment_id", sa.Integer(), nullable=False),
        sa.Column("old_status", sa.String(), nullable=True),
        sa.Column("new_status", sa.String(), nullable=False),
        sa.Column(
            "changed_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_shipment_audit_shipment_id"),
        "shipment_audit",
        ["shipment_id"],
        unique=False,
    )

    # Trigger: log status changes to shipment_audit
    op.execute(
        """
        CREATE OR REPLACE FUNCTION log_shipment_status_change()
        RETURNS TRIGGER AS $$
        BEGIN
            IF OLD.status IS DISTINCT FROM NEW.status THEN
                INSERT INTO shipment_audit (
                    shipment_id, old_status, new_status, changed_at
                )
                VALUES (NEW.id, OLD.status::text, NEW.status::text, now());
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trigger_shipment_status_audit
        AFTER UPDATE ON shipments
        FOR EACH ROW
        EXECUTE FUNCTION log_shipment_status_change();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trigger_shipment_status_audit ON shipments")
    op.execute("DROP FUNCTION IF EXISTS log_shipment_status_change()")

    op.drop_index(op.f("ix_shipment_audit_shipment_id"), table_name="shipment_audit")
    op.drop_table("shipment_audit")

    op.drop_index(op.f("ix_shipments_booking_id"), table_name="shipments")
    op.drop_table("shipments")
    op.execute("DROP TYPE IF EXISTS shipmentstatus")
