from fastapi.testclient import TestClient
from main import app, Base, engine
from sqlalchemy.orm import Session
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_task():
    response = client.post("/tasks/", json={"text": "Test task"})
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Test task"
    assert data["completed"] == False
    assert "id" in data

def test_read_tasks():
    # Create a task first
    client.post("/tasks/", json={"text": "Test task"})
    
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["text"] == "Test task"

def test_read_task():
    # Create a task first
    create_response = client.post("/tasks/", json={"text": "Test task"})
    task_id = create_response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Test task"
    assert data["id"] == task_id

def test_update_task():
    # Create a task first
    create_response = client.post("/tasks/", json={"text": "Test task"})
    task_id = create_response.json()["id"]
    
    response = client.put(f"/tasks/{task_id}", json={"text": "Updated task"})
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Updated task"
    assert data["id"] == task_id

def test_delete_task():
    # Create a task first
    create_response = client.post("/tasks/", json={"text": "Test task"})
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # Verify task is deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404 