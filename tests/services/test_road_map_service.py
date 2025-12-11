import pytest
from unittest.mock import patch, MagicMock
import overpy
from app.services.road_map_service import get_road_map, RoadMapError

def mock_overpass_result():
    node1 = MagicMock(lon="20.123", lat="50.123")
    node2 = MagicMock(lon="20.124", lat="50.124")

    way = MagicMock()
    way.id = 123
    way.nodes = [node1, node2]
    way.tags = {"highway": "residential", "name": "Test Street"}

    result = MagicMock()
    result.ways = [way]

    return result


@patch("app.services.road_map_service.api.query")
def test_get_road_map_success(mock_query):
    mock_query.return_value = mock_overpass_result()

    start = (50.0, 20.0)
    end = (50.001, 20.001)

    result = get_road_map(start, end)

    assert "features" in result
    assert len(result["features"]) == 1

    feature = result["features"][0]
    assert feature["properties"]["id"] == 123
    assert feature["properties"]["highway"] == "residential"

    coords = feature["geometry"]["coordinates"]
    assert coords == [
        [20.123, 50.123],
        [20.124, 50.124],
    ]


@patch("app.services.road_map_service.api.query")
def test_bounding_box_indirectly(mock_query):
    mock_query.return_value = mock_overpass_result()

    get_road_map((50.0, 20.0), (51.0, 21.0), margin=0.01)

    query_str = mock_query.call_args[0][0]

    assert "(49.99,19.99,51.01,21.01)" in query_str


@patch("app.services.road_map_service.api.query")
def test_get_road_map_too_many_requests(mock_query):
    mock_query.side_effect = overpy.exception.OverpassTooManyRequests()

    with pytest.raises(RoadMapError) as exc:
        get_road_map((50, 20), (51, 21))

    assert "Too many requests" in str(exc.value)


@patch("app.services.road_map_service.api.query")
def test_get_road_map_gateway_timeout(mock_query):
    mock_query.side_effect = overpy.exception.OverpassGatewayTimeout()

    with pytest.raises(RoadMapError) as exc:
        get_road_map((50, 20), (51, 21))

    assert "gateway timeout" in str(exc.value)


@patch("app.services.road_map_service.api.query")
def test_get_road_map_bad_request(mock_query):
    mock_query.side_effect = overpy.exception.OverpassBadRequest("Invalid query")

    with pytest.raises(RoadMapError) as exc:
        get_road_map((50, 20), (51, 21))

    assert "Bad request" in str(exc.value)


@patch("app.services.road_map_service.api.query")
def test_get_road_map_unexpected_error(mock_query):
    mock_query.side_effect = RuntimeError("Something failed")

    with pytest.raises(RoadMapError) as exc:
        get_road_map((50, 20), (51, 21))

    assert "Unexpected error" in str(exc.value)
