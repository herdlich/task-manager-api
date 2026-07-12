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
