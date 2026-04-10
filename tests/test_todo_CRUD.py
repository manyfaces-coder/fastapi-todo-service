def test_get_todo_by_id(client, auth_headers, created_todo):
    response = client.get(
        f"/todos/{created_todo['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_todo["id"]
    assert data["title"] == created_todo["title"]


def test_put_todo(client, auth_headers, created_todo):
    response = client.put(
        f"/todos/{created_todo['id']}",
        headers=auth_headers,
        json={
            "title": "Test todo after PUT",
            "description": "Test description 22",
            "completed": False,
            "version": created_todo["version"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_todo["id"]
    assert data["title"] == "Test todo after PUT"
    assert data["description"] == "Test description 22"


def test_patch_todo(client, auth_headers, created_todo):
    response = client.patch(
        f"/todos/{created_todo['id']}",
        headers=auth_headers,
        json={
            "description": "Test description after PATCH",
            "version": created_todo["version"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test description after PATCH"


def test_get_todo_by_id_after_delete(client, auth_headers, created_todo):
    delete_response = client.delete(
        f"/todos/{created_todo['id']}",
        headers=auth_headers,
    )
    assert delete_response.status_code == 200

    get_response = client.get(
        f"/todos/{created_todo['id']}",
        headers=auth_headers,
    )
    assert get_response.status_code == 404