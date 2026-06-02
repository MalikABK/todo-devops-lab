from fastapi.testclient import TestClient
from main import app, todos

client = TestClient(app)


def setup_function():
    """
    Clear in-memory todos before every test.
    This keeps each test independent.
    """
    todos.clear()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_todos_initially_empty():
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []


def test_create_todo():
    response = client.post(
        "/todos",
        json={"title": "Learn Docker"}
    )

    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Learn Docker"
    assert data["completed"] is False
    assert "id" in data


def test_get_todos_after_creating_todo():
    client.post("/todos", json={"title": "Learn FastAPI"})

    response = client.get("/todos")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Learn FastAPI"
    assert data[0]["completed"] is False


def test_update_todo_title():
    create_response = client.post(
        "/todos",
        json={"title": "Old title"}
    )

    todo_id = create_response.json()["id"]

    update_response = client.patch(
        f"/todos/{todo_id}",
        json={"title": "New title"}
    )

    data = update_response.json()

    assert update_response.status_code == 200
    assert data["title"] == "New title"
    assert data["completed"] is False


def test_update_todo_completed_status():
    create_response = client.post(
        "/todos",
        json={"title": "Learn CI/CD"}
    )

    todo_id = create_response.json()["id"]

    update_response = client.patch(
        f"/todos/{todo_id}",
        json={"completed": True}
    )

    data = update_response.json()

    assert update_response.status_code == 200
    assert data["title"] == "Learn CI/CD"
    assert data["completed"] is True


def test_delete_todo():
    create_response = client.post(
        "/todos",
        json={"title": "Delete this todo"}
    )

    todo_id = create_response.json()["id"]

    delete_response = client.delete(f"/todos/{todo_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Todo deleted"

    get_response = client.get("/todos")

    assert get_response.status_code == 200
    assert get_response.json() == []


def test_update_non_existing_todo_returns_404():
    response = client.patch(
        "/todos/fake-id",
        json={"title": "Updated title"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_delete_non_existing_todo_returns_404():
    response = client.delete("/todos/fake-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"