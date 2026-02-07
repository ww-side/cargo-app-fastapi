from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database.init import get_db
from app.features.bookings.schema import BookingCreate, BookingResponse
from app.features.bookings.service import BookingService
from app.shared.api_response import api_response

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/", response_model=dict)
def list_bookings(db: Session = Depends(get_db)):
    bookings = BookingService.list_all(db)
    data = [BookingResponse.model_validate(b) for b in bookings]
    return api_response(data)


@router.get("/{booking_id}", response_model=dict)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = BookingService.get_by_id(db, booking_id)
    return api_response(BookingResponse.model_validate(booking))


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    booking = BookingService.create(db, payload)
    return api_response(BookingResponse.model_validate(booking))


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    BookingService.delete(db, booking_id)
