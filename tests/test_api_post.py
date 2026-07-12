def test_post(client):
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
