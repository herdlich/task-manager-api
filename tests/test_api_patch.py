def test_patch(client, payload):
    for task in payload:
        client.post(
            "/tasks",
            json=task
        )

    patch_payload = {
        "description": "Cheese, butter"
    }

    response = client.patch(
        "/tasks/1",
        json=patch_payload
    )

    expected_response = {
        "id": 1,
        "title": "List of products",
        "description": "Cheese, butter",
        "due_date": "2026-07-12",
    }

    assert response.status_code == 200
    assert response.json() == expected_response


def test_patch_nonexistent_task(client, payload):
    for task in payload:
        client.post(
            "/tasks",
            json=task
        )

    patch_payload = {
        "description": "Cheese, butter"
    }

    response = client.patch(
        "/tasks/999",
        json=patch_payload
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "No task found"}


def test_patch_null_title(client, payload):
    for task in payload:
        client.post("/tasks",
                    json=task)

    response_patch = client.patch(
        "/tasks/1",
        json={"title": None}
    )

    assert response_patch.status_code == 422

    errors = response_patch.json()["detail"]

    assert any(
        error["loc"] == ["body", "title"]
        and error["input"] is None
        for error in errors
    )

    response_get = client.get("/tasks")

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

    assert response_get.status_code == 200
    assert response_get.json() == expected_response
