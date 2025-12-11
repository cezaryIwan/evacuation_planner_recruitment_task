from typing import Tuple, Dict, Any
from app.services.road_map_service import get_road_map

def evaluate_evac_route(start_coords: Tuple[float, float], end_coords: Tuple[float, float]) -> Dict[str, Any]:
    road_map = get_road_map(start_coords, end_coords)
    road_with_flood_zones = flood_zones_service.load_flood_zones(road_map)
    route_result = _evaluate_route(road_with_flood_zones, start_coords, end_coords)
    return _prepare_response(route_result)


def _evaluate_route(road_map: dict, start_coords: Tuple[float, float], end_coords: Tuple[float, float]) -> dict:
    return {
        "route": [],
        "metadata": {
            "length_m": 0,
            "segments_avoided": 0
        }
    }


def _prepare_response(route_result: dict) -> Dict[str, Any]:
    geojson = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": route_result.get("route", [])
        },
        "properties": route_result.get("metadata", {})
    }
    return geojson
