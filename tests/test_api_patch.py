def test_patch(client):
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

    patch_payload = {
        "description": "Cheese, butter"
    }

    response = client.patch(
        "/tasks/1",
        json=patch_payload
    )

    excepted_response = {
        "id": 1,
        "title": "List of products",
        "description": "Cheese, butter",
        "due_date": "2026-07-12",
    }

    assert response.status_code == 200
    assert response.json() == excepted_response
