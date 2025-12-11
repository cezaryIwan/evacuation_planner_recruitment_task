from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Tuple
from app.services.evac_route_service import EvacRouteService

router = APIRouter(prefix="/api/evac", tags=["evacuation"])


class CoordParser:
    def parse(self, raw: str) -> Tuple[float, float]:
        parts = raw.split(",")
        if len(parts) != 2:
            raise ValueError("Coordinate must be in format 'lat,lon'")

        try:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
        except ValueError:
            raise ValueError("Latitude and longitude must be valid numeric values")

        return lat, lon


def get_evac_service() -> EvacRouteService:
    return EvacRouteService()


def get_coord_parser() -> CoordParser:
    return CoordParser()


@router.get("/route")
def get_evacuation_route(
    start: str = Query(..., description="Latitude and Longitude of starting point"),
    end: str = Query(..., description="Latitude and Longitude of ending point"),
    service: EvacRouteService = Depends(get_evac_service),
    parser: CoordParser = Depends(get_coord_parser),
):
    try:
        start_coords = parser.parse(start)
        end_coords = parser.parse(end)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    return service.evaluate_evac_route(start_coords, end_coords)
