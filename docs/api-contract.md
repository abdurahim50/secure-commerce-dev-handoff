# API Contract

## Catalog Service

### `GET /healthz`

Returns service health.

Example response:

```json
{"status":"ok","service":"catalog-service"}
```

### `GET /readyz`

Returns readiness state.

Example response:

```json
{"status":"ready","service":"catalog-service"}
```

### `GET /products`

Returns available products.

Optional query parameter:

- `min_quantity`: integer, minimum available quantity

### `GET /products/{sku}`

Returns one product by SKU.

404 if SKU does not exist.

## Orders Service

### `GET /healthz`

Returns service health.

Example response:

```json
{"status":"ok","service":"orders-service"}
```

### `GET /readyz`

Returns readiness state.

Example response:

```json
{"status":"ready","service":"orders-service"}
```

### `POST /orders`

Creates an order after validating the SKU with catalog-service.

Request body:

```json
{
  "customer_id": "cust-1001",
  "sku": "LAPTOP-001",
  "quantity": 1
}
```

Expected success status: `201 Created`

### `GET /orders`

Lists current in-memory orders.

### `GET /orders/{order_id}`

Returns one order by ID.

404 if order does not exist.
