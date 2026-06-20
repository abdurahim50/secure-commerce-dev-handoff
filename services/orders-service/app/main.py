import os
from enum import StrEnum
from uuid import uuid4

import httpx
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://localhost:8001")

app = FastAPI(
    title="Orders Service",
    description="Order management microservice for Secure Commerce.",
    version="1.0.0",
)


class OrderStatus(StrEnum):
    CREATED = "created"
    REJECTED = "rejected"


class OrderCreate(BaseModel):
    customer_id: str = Field(..., min_length=3, examples=["cust-1001"])
    sku: str = Field(..., min_length=3, examples=["LAPTOP-001"])
    quantity: int = Field(..., ge=1, le=100, examples=[1])


class Order(BaseModel):
    order_id: str
    customer_id: str
    sku: str
    quantity: int
    unit_price: float
    total: float
    status: OrderStatus


ORDERS: dict[str, Order] = {}


async def lookup_catalog_product(sku: str) -> dict:
    timeout = httpx.Timeout(3.0, connect=1.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{CATALOG_SERVICE_URL}/products/{sku.upper()}")

    if response.status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=400, detail="SKU does not exist in catalog")
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail="Catalog service error")
    return response.json()


@app.get("/healthz", tags=["health"])
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "orders-service"}


@app.get("/readyz", tags=["health"])
def readyz() -> dict[str, str]:
    return {"status": "ready", "service": "orders-service"}


@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED, tags=["orders"])
async def create_order(payload: OrderCreate) -> Order:
    product = await lookup_catalog_product(payload.sku)
    quantity_available = int(product["quantity_available"])
    if payload.quantity > quantity_available:
        raise HTTPException(status_code=409, detail="Insufficient inventory")

    unit_price = float(product["price"])
    order = Order(
        order_id=str(uuid4()),
        customer_id=payload.customer_id,
        sku=payload.sku.upper(),
        quantity=payload.quantity,
        unit_price=unit_price,
        total=round(unit_price * payload.quantity, 2),
        status=OrderStatus.CREATED,
    )
    ORDERS[order.order_id] = order
    return order


@app.get("/orders/{order_id}", response_model=Order, tags=["orders"])
def get_order(order_id: str) -> Order:
    order = ORDERS.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/orders", response_model=list[Order], tags=["orders"])
def list_orders() -> list[Order]:
    return list(ORDERS.values())
