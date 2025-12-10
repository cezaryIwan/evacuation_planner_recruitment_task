from fastapi import APIRouter, HTTPException, Query
from typing import Tuple
from app.services.evac_route_service import evaluate_evac_route

router = APIRouter(prefix="/api/evac", tags=["evacuation"])

@router.get("/route")
def get_evacuation_route(
    start: str = Query(..., description="Latitude and Longitude of starting point"),
    end: str = Query(..., description="Latitude and Longitude of ending point"),
):
    try:
        start_coords = _parse_coords(start)
        end_coords = _parse_coords(end)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    return evaluate_evac_route(start_coords, end_coords)

def _parse_coords(raw: str) -> Tuple[float, float]:
    parts = raw.split(",")
    if len(parts) != 2:
        raise ValueError("Coordinate must be in format 'lat,lon'")
    try:
        lat = float(parts[0].strip())
        lon = float(parts[1].strip())
    except ValueError:
        raise ValueError("Latitude and longitude must be valid numeric values")

    return lat, lon