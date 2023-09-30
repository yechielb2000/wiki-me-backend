from fastapi.testclient import TestClient


def test_create_room():
    client = TestClient(app)
    with client.websocket_connect("/ws/yechiel/create-room") as websocket:
        data = websocket.receive_json()
        assert data is not None