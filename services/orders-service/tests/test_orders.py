import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_orders() -> None:
    main.ORDERS.clear()


def test_healthz_returns_ok() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_order(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_lookup_catalog_product(sku: str) -> dict:
        return {
            "sku": sku,
            "name": "Developer Laptop",
            "price": 1299.00,
            "quantity_available": 5,
        }

    monkeypatch.setattr(main, "lookup_catalog_product", fake_lookup_catalog_product)

    response = client.post(
        "/orders",
        json={"customer_id": "cust-1001", "sku": "LAPTOP-001", "quantity": 2},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["sku"] == "LAPTOP-001"
    assert body["total"] == 2598.00
    assert body["status"] == "created"


def test_rejects_order_when_inventory_is_low(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_lookup_catalog_product(sku: str) -> dict:
        return {
            "sku": sku,
            "name": "Developer Laptop",
            "price": 1299.00,
            "quantity_available": 1,
        }

    monkeypatch.setattr(main, "lookup_catalog_product", fake_lookup_catalog_product)

    response = client.post(
        "/orders",
        json={"customer_id": "cust-1001", "sku": "LAPTOP-001", "quantity": 2},
    )

    assert response.status_code == 409
