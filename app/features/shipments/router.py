from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database.init import get_db
from app.features.shipments.schema import (
    ShipmentAuditResponse,
    ShipmentCreate,
    ShipmentResponse,
    ShipmentUpdate,
)
from app.features.shipments.service import ShipmentService
from app.shared.api_response import api_response

router = APIRouter(prefix="/shipments", tags=["shipments"])


@router.get("/", response_model=dict)
def list_shipments(db: Session = Depends(get_db)):
    shipments = ShipmentService.list_all(db)
    return api_response([ShipmentResponse.model_validate(s) for s in shipments])


@router.get("/{shipment_id}", response_model=dict)
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = ShipmentService.get_by_id(db, shipment_id)
    return api_response(ShipmentResponse.model_validate(shipment))


@router.get("/{shipment_id}/audit", response_model=dict)
def get_shipment_audit(shipment_id: int, db: Session = Depends(get_db)):
    audit_records = ShipmentService.get_audit(db, shipment_id)
    return api_response(
        [ShipmentAuditResponse.model_validate(a) for a in audit_records]
    )


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_shipment(payload: ShipmentCreate, db: Session = Depends(get_db)):
    shipment = ShipmentService.create(db, payload)
    return api_response(ShipmentResponse.model_validate(shipment))


@router.patch("/{shipment_id}", response_model=dict)
def update_shipment_status(
    shipment_id: int, payload: ShipmentUpdate, db: Session = Depends(get_db)
):
    shipment = ShipmentService.update_status(db, shipment_id, payload)
    return api_response(ShipmentResponse.model_validate(shipment))
