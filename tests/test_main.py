from typing import Set
from fastapi.testclient import TestClient
from api.main import app
from api.config import Settings

client = TestClient(app)


def test_main_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "response": "/",
        "meta": {
            "limit": 0,
            "remaining": 0,
            "reset": 0,
            "used": 0,
        }
    }


def test_main_about():
    settings = Settings()
    response = client.get("/api/about")
    
    assert response.status_code == 200
    assert response.json() == {
        "app_name": settings.app_name,
        "created_by": settings.author,
        "admin_email": settings.admin_email,
        "meta": {
            "limit": 0,
            "remaining": 0,
            "reset": 0,
            "used": 0,
        }
    }