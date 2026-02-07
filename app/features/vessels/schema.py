import re
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

VESSEL_TYPE = Literal[
    "bulk_carrier",
    "container_ship",
    "tanker",
    "general_cargo",
    "roro",
    "lng_carrier",
    "lpg_carrier",
    "chemical_tanker",
    "other",
]


class VesselBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Vessel name")
    imo_number: str = Field(
        ..., min_length=10, max_length=10, description="IMO number (e.g. IMO8712345)"
    )
    max_capacity: float = Field(
        ..., gt=0, description="Maximum capacity in metric tons"
    )
    current_reserved_capacity: float = Field(
        0.0, ge=0, description="Currently reserved capacity"
    )
    vessel_type: VESSEL_TYPE = Field(..., description="Type of vessel")
    is_active: bool = Field(True, description="Whether the vessel is active")

    @field_validator("imo_number")
    @classmethod
    def validate_imo_number(cls, v: str) -> str:
        if not re.match(r"^IMO\d{7}$", v, re.IGNORECASE):
            raise ValueError(
                "IMO number must be in format IMO followed by 7 digits "
                "(e.g. IMO8712345)"
            )
        return v.upper()

    @model_validator(mode="after")
    def validate_reserved_capacity(self):
        if self.current_reserved_capacity > self.max_capacity:
            raise ValueError("current_reserved_capacity cannot exceed max_capacity")
        return self


class VesselCreate(VesselBase):
    pass


class VesselUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    imo_number: Optional[str] = Field(None, min_length=10, max_length=10)
    max_capacity: Optional[float] = Field(None, gt=0)
    current_reserved_capacity: Optional[float] = Field(None, ge=0)
    vessel_type: Optional[VESSEL_TYPE] = None
    is_active: Optional[bool] = None

    @field_validator("imo_number")
    @classmethod
    def validate_imo_number(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r"^IMO\d{7}$", v, re.IGNORECASE):
            raise ValueError(
                "IMO number must be in format IMO followed by 7 digits "
                "(e.g. IMO8712345)"
            )
        return v.upper()


class VesselResponse(BaseModel):
    id: int
    name: str
    imo_number: str
    max_capacity: float
    current_reserved_capacity: float
    vessel_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
