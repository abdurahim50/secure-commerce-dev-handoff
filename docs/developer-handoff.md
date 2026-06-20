# Developer Handoff: SecureCommerce

## Request to Platform Team

The backend development team has completed version `0.1.0` of the SecureCommerce microservices application.

We need the Platform/DevOps team to prepare the application for delivery through development, staging, and production environments.

## Required Platform Work

Please create the following from scratch:

1. Containerization for each service
2. Local multi-service runtime using Docker Compose
3. CI workflow for pull requests
4. Security scanning workflow
5. Container image build and tagging strategy
6. Kubernetes manifests
7. Environment overlays for dev, staging, and production
8. Cloud registry integration
9. Deployment workflow
10. Smoke tests and production readiness checks

## Service Details

### catalog-service

- Language: Python
- Framework: FastAPI
- App entrypoint: `app.main:app`
- Suggested local port: `8001`
- Health endpoint: `/healthz`
- Readiness endpoint: `/readyz`

### orders-service

- Language: Python
- Framework: FastAPI
- App entrypoint: `app.main:app`
- Suggested local port: `8002`
- Health endpoint: `/healthz`
- Readiness endpoint: `/readyz`
- Required environment variable: `CATALOG_SERVICE_URL`

## Dependency Flow

```text
User/API client → orders-service → catalog-service
```

The orders service calls the catalog service before creating an order.

## Known Limitations

- In-memory data only
- No authentication
- No database
- No message queue
- No production observability
- No container or Kubernetes assets included
- No CI/CD included
- No cloud infrastructure included

These limitations are intentional for the first platform delivery sprint.
