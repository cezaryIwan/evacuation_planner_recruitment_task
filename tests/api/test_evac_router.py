from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)
ok_json = {"result": "ok"}

def test_get_route_valid_integer():
    with patch("app.api.evac_router.evaluate_evac_route") as mocked_service:
        mocked_service.return_value = ok_json
        response = client.get("/api/evac/route", params={"start": "10,20", "end": "30,40"})
        assert response.status_code == 200
        assert response.json() == ok_json


def test_get_route_valid_float():
    with patch("app.api.evac_router.evaluate_evac_route") as mocked_service:
        mocked_service.return_value = ok_json
        response = client.get("/api/evac/route", params={"start": "10.5,20.1", "end": "30.25,40.75"})
        assert response.status_code == 200
        assert response.json() == ok_json


def test_missing_comma():
    response = client.get("/api/evac/route", params={"start": "10", "end": "30,40"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Coordinate must be in format 'lat,lon'"


def test_too_many_commas():
    response = client.get("/api/evac/route", params={"start": "10,20,30", "end": "30,40"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Coordinate must be in format 'lat,lon'"


def test_empty_values():
    response = client.get("/api/evac/route", params={"start": ",", "end": "30,40"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Latitude and longitude must be valid numeric values"


def test_non_numeric_values():
    response = client.get("/api/evac/route", params={"start": "30,40", "end": "abc,def"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Latitude and longitude must be valid numeric values"


def test_mixed_numeric_non_numeric():
    response = client.get("/api/evac/route", params={"start": "10,abc", "end": "30,40"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Latitude and longitude must be valid numeric values"


def test_missing_start_param():
    response = client.get("/api/evac/route", params={"end": "30,40"})
    assert response.status_code == 422