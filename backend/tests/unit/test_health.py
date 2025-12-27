import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_endpoint(client):
    """Test the health endpoint returns correct response"""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "status" in data["data"]
    assert data["data"]["status"] == "healthy"
    assert "dependencies" in data["data"]
    assert "timestamp" in data


def test_readiness_endpoint(client):
    """Test the readiness endpoint returns correct response"""
    response = client.get("/ready")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ready"