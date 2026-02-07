from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.shared.ports import AVAILABLE_PORTS


class BookingCreate(BaseModel):
    vessel_id: int = Field(..., gt=0, description="Vessel to book")
    reserved_capacity: float = Field(
        ..., gt=0, description="Capacity to reserve (metric tons)"
    )
    start_time: datetime = Field(..., description="Booking start (port arrival)")
    end_time: datetime = Field(..., description="Booking end (port departure)")
    port_name: AVAILABLE_PORTS = Field(..., description="Port name")

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class BookingResponse(BaseModel):
    id: int
    vessel_id: int
    reserved_capacity: float
    start_time: datetime
    end_time: datetime
    port_name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
