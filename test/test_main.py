from fastapi.testclient import TestClient
from api.main import app


client = TestClient(app)


def test_get_bus_around():
    response = client.post("/api/v1/busaround",
                           json={"latitude_from": 60, "latitude_to": 62, "longitude_from": 24, "longitude_to": 25})
    assert response.status_code == 200
