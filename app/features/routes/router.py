from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database.init import get_db
from app.features.routes.schema import RouteCreate, RouteResponse, RouteUpdate
from app.features.routes.service import RouteService
from app.shared.api_response import api_response

router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("/", response_model=dict)
def list_routes(db: Session = Depends(get_db)):
    routes = RouteService.list_all(db)
    data = [RouteResponse.model_validate(r) for r in routes]
    return api_response(data)


@router.get("/{route_id}", response_model=dict)
def get_route(route_id: int, db: Session = Depends(get_db)):
    route = RouteService.get_by_id(db, route_id)
    return api_response(RouteResponse.model_validate(route))


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_route(payload: RouteCreate, db: Session = Depends(get_db)):
    route = RouteService.create(db, payload)
    return api_response(RouteResponse.model_validate(route))


@router.patch("/{route_id}", response_model=dict)
def update_route(route_id: int, payload: RouteUpdate, db: Session = Depends(get_db)):
    route = RouteService.update(db, route_id, payload)
    return api_response(RouteResponse.model_validate(route))


@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_route(route_id: int, db: Session = Depends(get_db)):
    RouteService.delete(db, route_id)
