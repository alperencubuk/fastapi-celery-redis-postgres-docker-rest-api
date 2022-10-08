from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_task_add_user():
    response = client.post("/users/1")
    content = response.json()
    task_id = content["task_id"]
    assert task_id

    response = client.get(f"tasks/{task_id}")
    content = response.json()
    assert content == {"state": "PENDING"}
    assert response.status_code == 200

    while content["state"] == "PENDING":
        response = client.get(f"tasks/{task_id}")
        content = response.json()
    assert content == {"state": "SUCCESS"}


def test_task_add_weather():
    response = client.post("/weathers/erzincan")
    content = response.json()
    task_id = content["task_id"]
    assert task_id

    response = client.get(f"tasks/{task_id}")
    content = response.json()
    assert content == {"state": "PENDING"}
    assert response.status_code == 200

    while content["state"] == "PENDING":
        response = client.get(f"tasks/{task_id}")
        content = response.json()
    assert content == {"state": "SUCCESS"}
