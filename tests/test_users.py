import re

from fastapi.testclient import TestClient

from app.dependencies import user_repository
from app.main import app


client = TestClient(app)


def setup_function() -> None:
    user_repository.clear()


def test_user_crud_flow() -> None:
    created = client.post(
        "/users",
        json={"name": "Aman", "email": "aman@example.com", "age": 24},
    )
    assert created.status_code == 201
    user_id = created.json()["id"]
    assert re.fullmatch(r"user\d{6}", user_id)

    assert client.get(f"/users/{user_id}").status_code == 200
    assert client.patch(f"/users/{user_id}", json={"age": 25}).json()["age"] == 25
    assert client.delete(f"/users/{user_id}").status_code == 204
    assert client.get(f"/users/{user_id}").status_code == 404


def test_duplicate_email_returns_conflict() -> None:
    payload = {"name": "Aman", "email": "aman@example.com", "age": 24}
    assert client.post("/users", json=payload).status_code == 201

    response = client.post("/users", json=payload)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "EMAIL_ALREADY_EXISTS"

