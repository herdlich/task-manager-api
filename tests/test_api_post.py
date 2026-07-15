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

    assert response.status_code == 201
    assert response.json() == expected_response


def test_post_empty_title(client):
    payload = {
        "title": "",
        "description": "Milk, eggs, bread",
        "due_date": "2026-07-12",
    }

    response = client.post(
        "/tasks",
        json=payload
    )

    data = response.json()

    assert response.status_code == 422
    assert data["detail"][0]["type"] == "string_too_short"
    assert data["detail"][0]["loc"] == ["body", "title"]
    assert data["detail"][0]["input"] == ""

    check_response = client.get("/tasks")

    assert check_response.json() == []


def test_create_task_with_whitespace_title_returns_422(client):
    payload = {
        "title": " ",
        "description": "Milk, eggs, bread",
        "due_date": "2026-07-12",
    }

    response = client.post(
        "/tasks",
        json=payload
    )

    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["type"] == "string_too_short"
    assert data["detail"][0]["loc"] == ["body", "title"]
    assert data["detail"][0]["input"] == " "

    check_response = client.get("/tasks")

    assert check_response.status_code == 200
    assert check_response.json() == []


def test_create_task_with_wrong_date_format_returns_422(client):
    payload = {
        "title": "List of products",
        "description": "Milk, eggs, bread",
        "due_date": "12.07.26",
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422
    data = response.json()

    assert data["detail"][0]["type"] == "date_from_datetime_parsing"
    assert data["detail"][0]["loc"] == ["body", "due_date"]
    assert data["detail"][0]["input"] == "12.07.26"


def test_create_task_with_out_of_range_date_returns_422(client):
    payload = {
        "title": "List of products",
        "description": "Milk, eggs, bread",
        "due_date": "2028-13-32",
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422
    data = response.json()

    assert data["detail"][0]["type"] == "date_from_datetime_parsing"
    assert data["detail"][0]["loc"] == ["body", "due_date"]
    assert data["detail"][0]["input"] == "2028-13-32"
