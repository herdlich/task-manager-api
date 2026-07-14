import sqlite3

from task_manager_api.database import (
    db_init,
    save_db,
    get_all_tasks,
    get_task_by_id,
    delete_task_from_db,
    patch_task_by_id
)

from task_manager_api.models import TaskCreate


def test_db_init_creates_tasks_table(tmp_path):
    db_file = tmp_path / "data" / "tasks.db"

    db_init(db_file)

    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE TYPE = 'table' AND name = 'tasks'""")

        table = cursor.fetchone()

    assert table is not None
    assert table[0] == "tasks"


def test_save_to_db_adds_tasks(tmp_path):
    db_file = tmp_path / "data" / "tasks.db"

    payload = {
        "title": "List of products",
        "description": "Milk, eggs, bread",
        "due_date": "2026-07-12",
    }

    task = TaskCreate(**payload)

    db_init(db_file)
    created_task = save_db(db_file, task)

    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, title, description, due_date "
            "FROM tasks "
            "WHERE id = ?",
            (created_task["id"],)
        )

        row = cursor.fetchone()

    expected_row = (created_task["id"], 'List of products', 'Milk, eggs, bread', '2026-07-12')

    assert row is not None
    assert row == expected_row


def test_db_get_all_tasks(tmp_path, payload):
    db_file = tmp_path / "data" / "tasks.db"

    db_init(db_file)

    for item in payload:
        task = TaskCreate(**item)
        save_db(db_file, task)

    tasks = get_all_tasks(db_file)

    expected_task = [
        {
            "id": 1,
            "title": "List of products",
            "description": "Milk, eggs, bread",
            "due_date": "2026-07-12",
        },
        {
            "id": 2,
            "title": "Monthly Book List",
            "description": "Myth of Sisyphus, A. Camus; Demons, F. Dostoevsky",
            "due_date": "2026-07-12",
        }
    ]

    assert len(tasks) == 2
    assert tasks == expected_task


def test_db_empty_tasks(tmp_path):
    db_file = tmp_path / "data" / "tasks.db"
    db_init(db_file)

    tasks = get_all_tasks(db_file)

    assert tasks == []


def test_get_task_db_by_id(tmp_path, payload):
    db_file = tmp_path / "data" / "tasks.db"

    db_init(db_file)

    for item in payload:
        task = TaskCreate(**item)
        save_db(db_file, task)

    task_by_id = get_task_by_id(db_file, 2)

    expected_data = {
        "id": 2,
        "title": "Monthly Book List",
        "description": "Myth of Sisyphus, A. Camus; Demons, F. Dostoevsky",
        "due_date": "2026-07-12",
    }

    assert task_by_id == expected_data


def test_delete_db_task_by_id(tmp_path, payload):
    db_file = tmp_path / "data" / "tasks.db"

    db_init(db_file)

    for item in payload:
        task = TaskCreate(**item)
        save_db(db_file, task)

    delete_task_from_db(db_file, 1)

    updated_tasks = get_all_tasks(db_file)

    expected_data = [
        {
            "id": 2,
            "title": "Monthly Book List",
            "description": "Myth of Sisyphus, A. Camus; Demons, F. Dostoevsky",
            "due_date": "2026-07-12",
        }
    ]

    assert updated_tasks == expected_data


def test_patch_db_task(tmp_path, payload):
    db_file = tmp_path / "data" / "tasks.db"

    db_init(db_file)

    for item in payload:
        task = TaskCreate(**item)
        save_db(db_file, task)

    patch_changes = {"description": "Cheese, butter"}

    patch_task_by_id(db_file, 1, patch_changes)

    updated_task = get_task_by_id(db_file, 1)

    expected_data = {
        "id": 1,
        "title": "List of products",
        "description": "Cheese, butter",
        "due_date": "2026-07-12",
    }

    assert updated_task == expected_data