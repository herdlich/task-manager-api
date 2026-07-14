import sqlite3
from pathlib import Path
from contextlib import closing
from task_manager_api.models import TaskCreate, TaskUpdate


def db_init(db_file):
    Path(db_file).parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(db_file)

    with closing(connection) as db:
        with db:
            cursor = connection.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT
                )
            """)


def save_db(db_file, task: TaskCreate):
    connection = sqlite3.connect(db_file)

    query = """INSERT INTO tasks (title, description, due_date)
    VALUES(?, ?, ?)
    """

    values = (
        task.title,
        task.description,
        task.due_date.isoformat() if task.due_date else None
    )

    with closing(connection) as db:
        with db:
            cursor = connection.cursor()

            cursor.execute(query, values)

            task_id = cursor.lastrowid

    return {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "due_date": task.due_date
    }


def get_all_tasks(db_file):
    Path(db_file).parent.mkdir(exist_ok=True)
    connection = sqlite3.connect(db_file)

    connection.row_factory = sqlite3.Row

    with closing(connection) as db:
        with db:
            cursor = db.cursor()

            cursor.execute("""
                SELECT id, title, description, due_date 
                FROM tasks
                ORDER BY id ASC
            """)

            rows = cursor.fetchall()

            tasks = [dict(row) for row in rows]

    return tasks


def get_task_by_id(db_file, task_id):
    Path(db_file).parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(db_file)

    connection.row_factory = sqlite3.Row

    with closing(connection) as db:
        with db:
            cursor = db.cursor()

            cursor.execute("""
                    SELECT id, title, description, due_date 
                    FROM tasks
                    WHERE id = ?
                """, (task_id,))

            row = cursor.fetchone()

    return dict(row) if row is not None else None


def delete_task_from_db(db_file, task_id):
    Path(db_file).parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(db_file)

    with closing(connection) as db:
        with db:
            cursor = db.cursor()

            cursor.execute("""
            DELETE FROM tasks WHERE id = ?
            """, (task_id,))


def patch_task_by_id(db_file, task_id, changes):
    if not changes:
        return

    Path(db_file).parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(db_file)

    set_clause = ", ".join([f"{key} = ?" for key in changes.keys()])
    query_values = list(changes.values()) + [task_id]

    with closing(connection) as db:
        with db:
            cursor = db.cursor()

            cursor.execute(f"""
                UPDATE tasks
                SET {set_clause}
                WHERE id = ?
                """, query_values)
