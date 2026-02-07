from __future__ import annotations

from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.init import Base

if TYPE_CHECKING:
    from app.features.bookings.model import Booking


class ShipmentStatus(str, PyEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    booking_id: Mapped[int] = mapped_column(
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[ShipmentStatus] = mapped_column(
        Enum(ShipmentStatus),
        nullable=False,
        default=ShipmentStatus.PENDING,
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    booking: Mapped["Booking"] = relationship("Booking", back_populates="shipments")


class ShipmentAudit(Base):
    __tablename__ = "shipment_audit"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shipment_id: Mapped[int] = mapped_column(nullable=False, index=True)
    old_status: Mapped[str] = mapped_column(nullable=True)
    new_status: Mapped[str] = mapped_column(nullable=False)
    changed_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
