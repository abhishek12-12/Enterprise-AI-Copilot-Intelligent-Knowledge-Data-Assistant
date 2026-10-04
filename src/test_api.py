from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ask_endpoint():
    response = client.post(
        "/ask",
        json={"question": "How many employees are in Bangalore?"}
    )

    assert response.status_code == 200
    assert "3 employees" in response.json()["answer"]