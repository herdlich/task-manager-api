def test_delete(client):
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

    for task in payload:
        client.post(
            "/tasks",
            json=task
        )

    response_delete = client.delete("/tasks/1")

    expected_deleted_response = {
        "id": 1,
        "title": "List of products",
        "description": "Milk, eggs, bread",
        "due_date": "2026-07-12",
    }

    assert response_delete.status_code == 200
    assert response_delete.json() == expected_deleted_response

    response_get = client.get("/tasks")

    expected_get_response = [
        {
            "id": 2,
            "title": "Monthly Book List",
            "description": "Myth of Sisyphus, A. Camus; Demons, F. Dostoevsky",
            "due_date": "2026-07-12",
        }
    ]

    assert response_get.status_code == 200
    assert response_get.json() == expected_get_response
