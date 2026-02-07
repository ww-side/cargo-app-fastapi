from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator

from app.shared.ports import AVAILABLE_PORTS


class LegCreate(BaseModel):
    sequence: int = Field(..., ge=0, description="Order of leg in route")
    origin_port: AVAILABLE_PORTS = Field(..., description="Origin port")
    destination_port: AVAILABLE_PORTS = Field(..., description="Destination port")
    vessel_id: Optional[int] = Field(
        None, gt=0, description="Vessel assigned to this leg"
    )

    @model_validator(mode="after")
    def validate_ports(self):
        if self.origin_port == self.destination_port:
            raise ValueError("origin_port and destination_port must be different")
        return self


class LegUpdate(BaseModel):
    sequence: Optional[int] = Field(None, ge=0)
    origin_port: Optional[AVAILABLE_PORTS] = None
    destination_port: Optional[AVAILABLE_PORTS] = None
    vessel_id: Optional[int] = Field(None, gt=0)

    @model_validator(mode="after")
    def validate_ports(self):
        origin = self.origin_port
        dest = self.destination_port
        if origin is not None and dest is not None and origin == dest:
            raise ValueError("origin_port and destination_port must be different")
        return self


class LegResponse(BaseModel):
    id: int
    route_id: int
    sequence: int
    origin_port: str
    destination_port: str
    vessel_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RouteCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    legs: List[LegCreate] = Field(
        ..., min_length=1, description="Ordered legs of the journey"
    )

    @model_validator(mode="after")
    def validate_leg_chain(self):
        legs = sorted(self.legs, key=lambda leg: leg.sequence)
        for i, leg in enumerate(legs):
            if i > 0 and legs[i - 1].destination_port != leg.origin_port:
                prev = legs[i - 1].destination_port
                raise ValueError(
                    f"Leg {leg.sequence}: origin_port must match previous leg's "
                    f"destination_port ({prev} -> {leg.origin_port})"
                )
        return self


class RouteUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)


class RouteResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    legs: List[LegResponse] = []

    model_config = {"from_attributes": True}
