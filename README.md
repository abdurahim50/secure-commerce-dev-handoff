# SecureCommerce DevOps Handoff

SecureCommerce is a two-service FastAPI microservices project used to practice real-world DevOps and DevSecOps workflows.

The project started as an application team handoff and was extended with production-style delivery assets, including Dockerfiles, Docker Compose, Makefile automation, security checks, and a GitHub Actions CI pipeline.

## Services

| Service           | Runtime               | Description                                                       | Local Port |
| ----------------- | --------------------- | ----------------------------------------------------------------- | ---------- |
| `catalog-service` | Python 3.12 / FastAPI | Provides product catalog APIs                                     | `8001`     |
| `orders-service`  | Python 3.12 / FastAPI | Creates and lists orders. Calls catalog-service to validate SKUs. | `8002`     |

## Architecture

```text
User/API Client
      |
      v
orders-service
      |
      v
catalog-service
```

`orders-service` depends on `catalog-service` through this environment variable:

```bash
CATALOG_SERVICE_URL=http://catalog-service:8000
```

When running locally without containers, use:

```bash
CATALOG_SERVICE_URL=http://localhost:8001
```

## Repository Structure

```text
secure-commerce-dev-handoff/
├── .github/workflows/ci.yml
├── docs/
│   ├── api-contract.md
│   └── developer-handoff.md
├── services/
│   ├── catalog-service/
│   │   ├── app/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── requirements-dev.txt
│   │   └── pyproject.toml
│   └── orders-service/
│       ├── app/
│       ├── tests/
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── requirements-dev.txt
│       └── pyproject.toml
├── docker-compose.yml
├── Makefile
├── README.md
└── .gitignore
```

## Prerequisites

Install the following tools:

* Python 3.12+
* Docker
* Docker Compose
* Git
* Make

Verify your tools:

```bash
python3 --version
docker --version
docker compose version
git --version
make --version
```

## Quick Start

Create the virtual environment and install dependencies:

```bash
make install
```

Run tests:

```bash
make test
```

Run lint checks:

```bash
make lint
```

Run security checks:

```bash
make security
```

Start the full application stack with Docker Compose:

```bash
make compose-up
```

Check service status:

```bash
make compose-ps
```

Stop the stack:

```bash
make compose-down
```

## Makefile Commands

| Command               | Description                                      |
| --------------------- | ------------------------------------------------ |
| `make help`           | Show available commands                          |
| `make venv`           | Create local Python virtual environment          |
| `make install`        | Install runtime and development dependencies     |
| `make test`           | Run all unit tests                               |
| `make lint`           | Run Ruff lint checks                             |
| `make bandit`         | Run Bandit security scans                        |
| `make audit`          | Run pip-audit dependency vulnerability scans     |
| `make security`       | Run Bandit and pip-audit                         |
| `make run-catalog`    | Run catalog-service locally on port 8001         |
| `make run-orders`     | Run orders-service locally on port 8002          |
| `make compose-config` | Validate Docker Compose configuration            |
| `make compose-up`     | Build and start all services with Docker Compose |
| `make compose-ps`     | Show Docker Compose service status               |
| `make compose-logs`   | Show Docker Compose logs                         |
| `make compose-down`   | Stop and remove Docker Compose services          |
| `make clean`          | Remove Python cache and test cache files         |
| `make clean-venv`     | Remove the local virtual environment             |

## API Endpoints

### Catalog Service

Base URL:

```text
http://localhost:8001
```

Endpoints:

```text
GET /healthz
GET /readyz
GET /products
GET /products/{sku}
```

Example:

```bash
curl http://localhost:8001/healthz
curl http://localhost:8001/products
```

### Orders Service

Base URL:

```text
http://localhost:8002
```

Endpoints:

```text
GET /healthz
GET /readyz
POST /orders
GET /orders
GET /orders/{order_id}
```

Example order request:

```bash
curl -X POST http://localhost:8002/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"cust-1001","sku":"LAPTOP-001","quantity":1}'
```

## Running Without Containers

Start catalog-service:

```bash
make run-catalog
```

In a second terminal, start orders-service:

```bash
make run-orders
```

Then test:

```bash
curl http://localhost:8001/healthz
curl http://localhost:8002/healthz
```

## Running With Docker Compose

Validate the Compose configuration:

```bash
make compose-config
```

Build and start both services:

```bash
make compose-up
```

Check service status:

```bash
make compose-ps
```

View logs:

```bash
make compose-logs
```

Stop and remove containers/network:

```bash
make compose-down
```

## Docker Images

Build catalog-service manually:

```bash
docker build -t secure-commerce/catalog-service:dev services/catalog-service
```

Build orders-service manually:

```bash
docker build -t secure-commerce/orders-service:dev services/orders-service
```

Both services run on port `8000` inside their containers.

Host port mapping through Docker Compose:

```text
catalog-service: localhost:8001 -> container port 8000
orders-service:  localhost:8002 -> container port 8000
```

## Security

This project includes DevSecOps checks:

```bash
make bandit
make audit
make security
```

Security tooling:

* `bandit` scans Python code for common security issues.
* `pip-audit` scans Python dependencies for known vulnerabilities.
* Containers run as a non-root user named `appuser`.

Verify container user:

```bash
make compose-up
docker compose exec catalog-service id
docker compose exec orders-service id
make compose-down
```

Expected user:

```text
uid=10001(appuser)
```

## Continuous Integration

GitHub Actions workflow:

```text
.github/workflows/ci.yml
```

The CI pipeline runs on:

* Pull requests into `main`
* Pushes to `main`
* Manual workflow dispatch

CI jobs:

1. Tests, lint, and security

   * Installs Python dependencies
   * Runs unit tests
   * Runs Ruff lint checks
   * Runs Bandit
   * Runs pip-audit

2. Container build and Compose validation

   * Builds catalog-service Docker image
   * Builds orders-service Docker image
   * Validates Docker Compose configuration

## Troubleshooting

### Docker daemon is not running

If Docker commands fail, start Docker Desktop or the Docker daemon.

Check Docker:

```bash
docker info
```

### Port already in use

If ports `8001` or `8002` are already being used, stop existing containers:

```bash
docker compose down
```

Check running containers:

```bash
docker ps
```

### Orders service cannot reach catalog service

When using Docker Compose, make sure the environment variable uses the Compose service name:

```bash
CATALOG_SERVICE_URL=http://catalog-service:8000
```

When running locally without containers, use:

```bash
CATALOG_SERVICE_URL=http://localhost:8001
```

### GitHub Actions fails on Docker Hub pull

If the base image cannot be pulled, check Docker Hub availability or authentication/rate limits.

The base image is:

```text
python:3.12-slim
```

## Current Status

Completed DevOps work:

* Git baseline and branch workflow
* Local Python validation
* Root Makefile automation
* Dockerfiles for both services
* Docker Compose runtime
* Security scans with Bandit and pip-audit
* GitHub Actions CI pipeline

## Notes

This project uses in-memory data only. Data does not persist after service restart.

There is no authentication, database, Kubernetes deployment, cloud infrastructure, monitoring stack, or production secrets management yet. These are future platform engineering enhancements.
