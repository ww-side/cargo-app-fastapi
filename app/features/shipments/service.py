from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.bookings.model import Booking
from app.features.shipments.model import Shipment, ShipmentAudit, ShipmentStatus
from app.features.shipments.schema import ShipmentCreate, ShipmentUpdate


class ShipmentService:
    @staticmethod
    def get_or_404(db: Session, shipment_id: int) -> Shipment:
        shipment = db.get(Shipment, shipment_id)
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment {shipment_id} not found",
            )
        return shipment

    @staticmethod
    def list_all(db: Session) -> List[Shipment]:
        result = db.execute(select(Shipment).order_by(Shipment.id))
        return list(result.scalars().all())

    @staticmethod
    def get_by_id(db: Session, shipment_id: int) -> Shipment:
        return ShipmentService.get_or_404(db, shipment_id)

    @staticmethod
    def get_audit(db: Session, shipment_id: int) -> List[ShipmentAudit]:
        ShipmentService.get_or_404(db, shipment_id)
        result = db.execute(
            select(ShipmentAudit)
            .where(ShipmentAudit.shipment_id == shipment_id)
            .order_by(ShipmentAudit.changed_at.asc())
        )
        return list(result.scalars().all())

    @staticmethod
    def create(db: Session, payload: ShipmentCreate) -> Shipment:
        booking = db.get(Booking, payload.booking_id)
        if booking is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Booking {payload.booking_id} not found",
            )
        shipment = Shipment(booking_id=payload.booking_id)
        db.add(shipment)
        db.commit()
        db.refresh(shipment)
        return shipment

    @staticmethod
    def update_status(
        db: Session, shipment_id: int, payload: ShipmentUpdate
    ) -> Shipment:
        shipment = ShipmentService.get_or_404(db, shipment_id)
        shipment.status = ShipmentStatus(payload.status)
        db.commit()
        db.refresh(shipment)
        return shipment
