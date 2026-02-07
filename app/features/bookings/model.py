from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.init import Base

if TYPE_CHECKING:
    from app.features.shipments.model import Shipment
    from app.features.vessels.model import Vessel


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vessel_id: Mapped[int] = mapped_column(
        ForeignKey("vessels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reserved_capacity: Mapped[float] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False
    )
    end_time: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False
    )
    port_name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    vessel: Mapped["Vessel"] = relationship("Vessel", back_populates="bookings")
    shipments: Mapped[list["Shipment"]] = relationship(
        "Shipment", back_populates="booking", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "reserved_capacity > 0",
            name="check_reserved_capacity_positive",
        ),
        CheckConstraint(
            "end_time > start_time",
            name="check_valid_time_range",
        ),
        ExcludeConstraint(
            ("vessel_id", "="),
            (func.tstzrange(start_time, end_time), "&&"),
            name="excl_vessel_no_overlapping_bookings",
            using="gist",
        ),
    )
