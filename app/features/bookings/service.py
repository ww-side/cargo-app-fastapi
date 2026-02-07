from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.features.bookings.model import Booking
from app.features.bookings.schema import BookingCreate
from app.features.vessels.model import Vessel


class BookingService:
    @staticmethod
    def get_or_404(db: Session, booking_id: int) -> Booking:
        booking = db.get(Booking, booking_id)
        if booking is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Booking {booking_id} not found",
            )
        return booking

    @staticmethod
    def list_all(db: Session) -> List[Booking]:
        stmt = select(Booking).order_by(Booking.start_time.desc())
        result = db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    def get_by_id(db: Session, booking_id: int) -> Booking:
        return BookingService.get_or_404(db, booking_id)

    @staticmethod
    def create(db: Session, payload: BookingCreate) -> Booking:
        stmt = select(Vessel).where(Vessel.id == payload.vessel_id).with_for_update()
        vessel = db.execute(stmt).scalar_one_or_none()

        if vessel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vessel {payload.vessel_id} not found",
            )
        if not vessel.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot book inactive vessel",
            )

        new_total = vessel.current_reserved_capacity + payload.reserved_capacity
        if new_total > vessel.max_capacity:
            available = vessel.max_capacity - vessel.current_reserved_capacity
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Insufficient capacity. Available: {available:.2f}",
            )

        booking = Booking(**payload.model_dump())
        db.add(booking)
        vessel.current_reserved_capacity = new_total

        try:
            db.commit()
            db.refresh(booking)
        except IntegrityError as e:
            db.rollback()
            err_msg = str(e.orig) if e.orig else str(e)
            if "excl_vessel_no_overlapping_bookings" in err_msg:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Vessel has overlapping booking for this time range",
                )
            raise

        return booking

    @staticmethod
    def delete(db: Session, booking_id: int) -> None:
        booking = BookingService.get_or_404(db, booking_id)
        vessel = booking.vessel
        vessel.current_reserved_capacity = max(
            0, vessel.current_reserved_capacity - booking.reserved_capacity
        )
        db.delete(booking)
        db.commit()
