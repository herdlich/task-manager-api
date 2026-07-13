import pytest
from fastapi.testclient import TestClient
from task_manager_api.api import app
import task_manager_api.api as api


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    api.task_list.clear()
    api.id_count = 1

    yield
    api.task_list.clear()
    api.id_count = 1


@pytest.fixture()
def payload():
    payload = [
        {
            "title": "List of products",
            "description": "Milk, eggs, bread",
            "due_date": "2026-07-12",
        },
        {
            "title": "Monthly Book List",
            "description": "Myth of Sisyphus, A. Camus; Demons, F. Dostoevsky",
            "due_date": "2026-07-12",
        },
    ]

    return payload
