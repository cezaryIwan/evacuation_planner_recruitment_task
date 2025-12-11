from typing import Tuple, Dict, Any
from app.services.road_map_service import get_road_map

def evaluate_evac_route(start, end):
    bbox = self._calculate_bbox(start, end)

    road_map = self.road_map_service.get_road_map(bbox)
    flood_zones = self.flood_zone_service.load_flood_zones(bbox)

    route = self.route_service.evaluate_route(road_map, flood_zones, start, end)

    return format_response(route)


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
