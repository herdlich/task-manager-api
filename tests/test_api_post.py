import pytest
from fastapi.testclient import TestClient
from task_manager_api.api import app
import task_manager_api.api as api

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    api.task_list.clear()
    api.id_count = 1

    yield
    api.task_list.clear()
    api.id_count = 1


def test_post():
    payload = {
        "title": "List of products",
        "description": "Milk, eggs, bread",
        "due_date": "2026-07-12",
    }

    response = client.post(
        "/tasks",
        json=payload
    )

    expected_response = {
        "id": 1,
        "title": "List of products",
        "description": "Milk, eggs, bread",
        "due_date": "2026-07-12",
    }

    assert response.status_code == 200
    assert response.json() == expected_response
