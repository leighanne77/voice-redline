import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import get_test_settings

settings = get_test_settings()
client = TestClient(app)

def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_docs_endpoint(client):
    """Test the documentation endpoint"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_openapi_schema(client):
    """Test the OpenAPI schema endpoint"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
