from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.init import Base

if TYPE_CHECKING:
    from app.features.vessels.model import Vessel


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    legs: Mapped[list["Leg"]] = relationship(
        "Leg",
        back_populates="route",
        order_by="Leg.sequence",
        cascade="all, delete-orphan",
    )


class Leg(Base):
    __tablename__ = "legs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    route_id: Mapped[int] = mapped_column(
        ForeignKey("routes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sequence: Mapped[int] = mapped_column(nullable=False)
    origin_port: Mapped[str] = mapped_column(nullable=False)
    destination_port: Mapped[str] = mapped_column(nullable=False)
    vessel_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("vessels.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    route: Mapped["Route"] = relationship("Route", back_populates="legs")
    vessel: Mapped[Optional["Vessel"]] = relationship("Vessel")

    __table_args__ = (
        CheckConstraint(
            "origin_port != destination_port",
            name="check_leg_different_ports",
        ),
    )
