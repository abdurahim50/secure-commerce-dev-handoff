from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(
    title="Catalog Service",
    description="Product catalog microservice for Secure Commerce.",
    version="1.0.0",
)


class Product(BaseModel):
    sku: str = Field(..., examples=["LAPTOP-001"])
    name: str
    price: float = Field(..., ge=0)
    quantity_available: int = Field(..., ge=0)


CATALOG: dict[str, Product] = {
    "LAPTOP-001": Product(
        sku="LAPTOP-001", name="Developer Laptop", price=1299.00, quantity_available=12
    ),
    "MONITOR-001": Product(
        sku="MONITOR-001", name="27-inch Security Monitor", price=349.00, quantity_available=20
    ),
    "KEYBOARD-001": Product(
        sku="KEYBOARD-001", name="Mechanical Keyboard", price=129.00, quantity_available=40
    ),
}


@app.get("/healthz", tags=["health"])
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "catalog-service"}


@app.get("/readyz", tags=["health"])
def readyz() -> dict[str, str]:
    return {"status": "ready", "service": "catalog-service"}


@app.get("/products", response_model=list[Product], tags=["catalog"])
def list_products(
    min_quantity: Annotated[int, Query(ge=0, description="Only return products with stock >= value")] = 0,
) -> list[Product]:
    return [product for product in CATALOG.values() if product.quantity_available >= min_quantity]


@app.get("/products/{sku}", response_model=Product, tags=["catalog"])
def get_product(sku: str) -> Product:
    product = CATALOG.get(sku.upper())
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
