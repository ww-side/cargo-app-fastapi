from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.features.routes.model import Leg, Route
from app.features.routes.schema import RouteCreate, RouteUpdate


class RouteService:
    @staticmethod
    def get_or_404(db: Session, route_id: int) -> Route:
        route = (
            db.execute(
                select(Route)
                .where(Route.id == route_id)
                .options(joinedload(Route.legs))
            )
            .unique()
            .scalar_one_or_none()
        )
        if route is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Route {route_id} not found",
            )
        return route

    @staticmethod
    def list_all(db: Session) -> List[Route]:
        stmt = select(Route).options(joinedload(Route.legs)).order_by(Route.id)
        result = db.execute(stmt)
        return list(result.unique().scalars().all())

    @staticmethod
    def get_by_id(db: Session, route_id: int) -> Route:
        return RouteService.get_or_404(db, route_id)

    @staticmethod
    def create(db: Session, payload: RouteCreate) -> Route:
        route = Route(name=payload.name)
        db.add(route)
        db.flush()
        sorted_legs = sorted(payload.legs, key=lambda leg: leg.sequence)
        for leg_data in sorted_legs:
            leg = Leg(
                route_id=route.id,
                sequence=leg_data.sequence,
                origin_port=leg_data.origin_port,
                destination_port=leg_data.destination_port,
                vessel_id=leg_data.vessel_id,
            )
            db.add(leg)
        db.commit()
        return RouteService.get_or_404(db, route.id)

    @staticmethod
    def update(db: Session, route_id: int, payload: RouteUpdate) -> Route:
        route = RouteService.get_or_404(db, route_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(route, key, value)
        db.commit()
        return RouteService.get_or_404(db, route.id)

    @staticmethod
    def delete(db: Session, route_id: int) -> None:
        route = RouteService.get_or_404(db, route_id)
        db.delete(route)
        db.commit()
