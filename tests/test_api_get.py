def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_all_tasks(client, payload):
    for task in payload:
        client.post(
            "/tasks",
            json=task
        )

    response = client.get("/tasks")

    expected_response = [
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
        },
    ]

    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_nonexistent_task(client, payload):
    for task in payload:
        client.post(
            "/tasks",
            json=task
        )

    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "No task found"}
