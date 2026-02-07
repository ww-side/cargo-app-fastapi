from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Index, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.init import Base

if TYPE_CHECKING:
    from app.features.bookings.model import Booking


class Vessel(Base):
    __tablename__ = "vessels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    imo_number: Mapped[str] = mapped_column(unique=True, index=True)

    max_capacity: Mapped[float] = mapped_column(nullable=False)
    current_reserved_capacity: Mapped[float] = mapped_column(default=0.0)

    vessel_type: Mapped[str] = mapped_column(index=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    bookings: Mapped[list["Booking"]] = relationship(
        "Booking",
        back_populates="vessel",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint(
            "current_reserved_capacity <= max_capacity", name="check_capacity_limit"
        ),
        CheckConstraint(
            "current_reserved_capacity >= 0", name="check_positive_capacity"
        ),
        Index("idx_active_vessels", "id", postgresql_where=text("is_active = true")),
    )
