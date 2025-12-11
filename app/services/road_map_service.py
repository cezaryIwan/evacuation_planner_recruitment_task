import overpy
from typing import Dict, Tuple


class RoadMapService:
def __init__(self, api_client=None):
    self.api = api_client or overpy.Overpass()

def get_road_map(self, start_coords: Tuple[float, float], end_coords: Tuple[float, float], margin=0.005) -> Dict:
    min_lat, min_lon, max_lat, max_lon = self._calculate_bounding_box(start_coords, end_coords, margin)
    return self._query_api(min_lat, min_lon, max_lat, max_lon)

def _calculate_bounding_box(self, start, end, margin):
    min_lat = min(start[0], end[0]) - margin
    max_lat = max(start[0], end[0]) + margin
    min_lon = min(start[1], end[1]) - margin
    max_lon = max(start[1], end[1]) + margin
    return min_lat, min_lon, max_lat, max_lon

def _query_api(self, min_lat, min_lon, max_lat, max_lon):
    query = f"""
    (
        way["highway"]({min_lat},{min_lon},{max_lat},{max_lon});
    );
    out body;
    >;
    out skel qt;
    """
    result = self.api.query(query)

    features = []
    for way in result.ways:
        coords = [[float(node.lon), float(node.lat)] for node in way.nodes]
        features.append({
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": {"id": way.id, "highway": way.tags.get("highway")}
        })

    return {"type": "FeatureCollection", "features": features}
