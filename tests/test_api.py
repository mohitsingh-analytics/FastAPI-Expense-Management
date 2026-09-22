from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_expense():
    payload = {
        "date":"2026-09-22",
        "category":"Food",
        "amount":500,
        "payment_method":"UPI",
        "description":"Lunch",
    }
    response= client.post("/expenses",json=payload)

    assert response.status_code==200
    assert response.json()["category"]=="Food"
    assert response.json()["amount"]==500


def test_create_expense_invalid_amount():
    payload = {
        "date": "2026-09-22",
        "category": "Food",
        "amount": "invalid",
        "payment_method": "UPI",
        "description": "Lunch",
    }

    response = client.post("/expenses", json=payload)

    assert response.status_code == 422