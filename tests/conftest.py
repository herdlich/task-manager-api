import pytest
from task_manager_api.database import db_init
from fastapi.testclient import TestClient
from task_manager_api.api import app


@pytest.fixture()
def client(monkeypatch, tmp_path):
    path_db = tmp_path / "data" / "tasks.db"
    monkeypatch.setattr(
        "task_manager_api.api.DB_PATH",
        path_db
    )

    db_init(path_db)

    return TestClient(app)


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
