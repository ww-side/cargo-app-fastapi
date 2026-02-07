from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database.init import get_db
from app.features.vessels.schema import VesselCreate, VesselResponse, VesselUpdate
from app.features.vessels.service import VesselService
from app.shared.api_response import api_response

router = APIRouter(prefix="/vessels", tags=["vessels"])


@router.get("/", response_model=dict)
def list_vessels(db: Session = Depends(get_db)):
    vessels = VesselService.list_all(db)
    data = [VesselResponse.model_validate(v) for v in vessels]
    return api_response(data)


@router.get("/{vessel_id}", response_model=dict)
def get_vessel(vessel_id: int, db: Session = Depends(get_db)):
    vessel = VesselService.get_by_id(db, vessel_id)
    return api_response(VesselResponse.model_validate(vessel))


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_vessel(payload: VesselCreate, db: Session = Depends(get_db)):
    vessel = VesselService.create(db, payload)
    return api_response(VesselResponse.model_validate(vessel))


@router.put("/{vessel_id}", response_model=dict)
def update_vessel(vessel_id: int, payload: VesselUpdate, db: Session = Depends(get_db)):
    vessel = VesselService.update(db, vessel_id, payload)
    return api_response(VesselResponse.model_validate(vessel))


@router.patch("/{vessel_id}", response_model=dict)
def partial_update_vessel(
    vessel_id: int, payload: VesselUpdate, db: Session = Depends(get_db)
):
    vessel = VesselService.update(db, vessel_id, payload)
    return api_response(VesselResponse.model_validate(vessel))


@router.delete("/{vessel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vessel(vessel_id: int, db: Session = Depends(get_db)):
    VesselService.delete(db, vessel_id)
