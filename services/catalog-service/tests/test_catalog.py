from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz_returns_ok() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_products_returns_seed_data() -> None:
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) >= 3


def test_get_product_by_sku() -> None:
    response = client.get("/products/LAPTOP-001")
    assert response.status_code == 200
    assert response.json()["sku"] == "LAPTOP-001"


def test_get_product_not_found() -> None:
    response = client.get("/products/DOES-NOT-EXIST")
    assert response.status_code == 404
