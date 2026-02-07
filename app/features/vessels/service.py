from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.vessels.model import Vessel
from app.features.vessels.schema import VesselCreate, VesselUpdate


class VesselService:
    @staticmethod
    def get_or_404(db: Session, vessel_id: int) -> Vessel:
        vessel = db.get(Vessel, vessel_id)
        if vessel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vessel with id {vessel_id} not found",
            )
        return vessel

    @staticmethod
    def list_all(db: Session) -> List[Vessel]:
        stmt = select(Vessel).order_by(Vessel.id)
        result = db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    def get_by_id(db: Session, vessel_id: int) -> Vessel:
        return VesselService.get_or_404(db, vessel_id)

    @staticmethod
    def create(db: Session, payload: VesselCreate) -> Vessel:
        stmt = select(Vessel).where(Vessel.imo_number == payload.imo_number)
        if db.execute(stmt).scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Vessel with IMO number {payload.imo_number} already exists",
            )
        vessel = Vessel(**payload.model_dump())
        db.add(vessel)
        db.commit()
        db.refresh(vessel)
        return vessel

    @staticmethod
    def update(db: Session, vessel_id: int, payload: VesselUpdate) -> Vessel:
        vessel = VesselService.get_or_404(db, vessel_id)
        update_data = payload.model_dump(exclude_unset=True)

        if "imo_number" in update_data:
            stmt = select(Vessel).where(
                Vessel.imo_number == update_data["imo_number"],
                Vessel.id != vessel_id,
            )
            if db.execute(stmt).scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"Vessel with IMO number {update_data['imo_number']} "
                        "already exists"
                    ),
                )

        max_cap = update_data.get("max_capacity", vessel.max_capacity)
        reserved = update_data.get(
            "current_reserved_capacity", vessel.current_reserved_capacity
        )
        if reserved > max_cap:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="current_reserved_capacity cannot exceed max_capacity",
            )

        for key, value in update_data.items():
            setattr(vessel, key, value)

        db.commit()
        db.refresh(vessel)
        return vessel

    @staticmethod
    def delete(db: Session, vessel_id: int) -> None:
        vessel = VesselService.get_or_404(db, vessel_id)
        db.delete(vessel)
        db.commit()
