from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

ShipmentStatus = Literal[
    "PENDING",
    "CONFIRMED",
    "SHIPPED",
    "IN_TRANSIT",
    "DELIVERED",
    "CANCELLED",
]


class ShipmentCreate(BaseModel):
    booking_id: int = Field(..., gt=0, description="Booking to create shipment for")


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus = Field(..., description="New status")


class ShipmentResponse(BaseModel):
    id: int
    booking_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ShipmentAuditResponse(BaseModel):
    id: int
    shipment_id: int
    old_status: Optional[str]
    new_status: str
    changed_at: datetime

    model_config = {"from_attributes": True}
