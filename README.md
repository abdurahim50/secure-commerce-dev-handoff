# SecureCommerce Developer Handoff

This repository represents the **application team handoff** for the SecureCommerce microservices project.

It intentionally contains only developer-owned application code, dependency files, tests, and API handoff documentation. DevOps/DevSecOps files such as Dockerfiles, Docker Compose, GitHub Actions workflows, Kubernetes manifests, cloud infrastructure, security policy, deployment scripts, and release automation are intentionally **not included**.

The Platform/DevOps team is expected to build those delivery assets from scratch.

## Application services

| Service | Runtime | Description | Local port suggestion |
|---|---|---|---|
| `catalog-service` | Python / FastAPI | Provides product catalog APIs | `8001` |
| `orders-service` | Python / FastAPI | Creates and lists orders. Calls catalog-service to validate SKUs. | `8002` |

## Service ownership

The development team owns:

- FastAPI application code under `services/*/app/`
- Unit tests under `services/*/tests/`
- Python dependency files
- API behavior and service contracts

The DevOps/DevSecOps team will own, create, and maintain:

- Dockerfiles
- Docker Compose
- CI/CD workflows
- Security scans
- Kubernetes manifests
- Cloud infrastructure
- Deployment scripts
- Secrets and environment strategy
- Release and rollback process
- Monitoring and production operations

## API summary

### Catalog service

Base URL in local development: `http://localhost:8001`

Endpoints:

- `GET /healthz`
- `GET /readyz`
- `GET /products`
- `GET /products/{sku}`

### Orders service

Base URL in local development: `http://localhost:8002`

Endpoints:

- `GET /healthz`
- `GET /readyz`
- `POST /orders`
- `GET /orders`
- `GET /orders/{order_id}`

The orders service depends on the catalog service through this environment variable:

```bash
CATALOG_SERVICE_URL=http://localhost:8001
```

## Run locally without DevOps tooling

This section is for application developers only. DevOps will later replace this with Docker, Compose, CI/CD, and Kubernetes workflows.

### Catalog service

```bash
cd services/catalog-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Orders service

Open a second terminal:

```bash
cd services/orders-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
export CATALOG_SERVICE_URL=http://localhost:8001
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

## Manual test examples

```bash
curl http://localhost:8001/healthz
curl http://localhost:8002/healthz
curl http://localhost:8001/products
curl -X POST http://localhost:8002/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"cust-1001","sku":"LAPTOP-001","quantity":1}'
```

## Unit tests

Run tests inside each service directory:

```bash
cd services/catalog-service
pytest
```

```bash
cd services/orders-service
pytest
```

## Developer handoff notes

- Both services expose `/healthz` and `/readyz`.
- Both services listen on port `8000` inside a future container, but developers commonly run them on `8001` and `8002` locally.
- `orders-service` must be configured with `CATALOG_SERVICE_URL`.
- Current storage is in-memory only. Data does not persist after restart.
- There is no authentication in this version.
- There is no database in this version.
- Production hardening is expected from the Platform/DevSecOps team.
