# Projects

Run these with Docker Compose. Do not install the Python dependencies on the host.

| Project | Port | What it proves |
| --- | --- | --- |
| [E-commerce REST API](ecommerce_rest_api/README.md) | 8000 | Auth, catalog, transactional orders, idempotency keys, object-level reads |
| [Asynchronous job API](asynchronous_job_api/README.md) | 8001 | Durable job rows, Redis wake-ups, cancel, retries toward a dead state |
| [Production AI API](production_ai_api/README.md) | 8002 | Mock model, SSE, tenant-scoped retrieval, tool allow-list, quotas |

Pytest has not been executed here because the Docker daemon was not running. Commands are in each project README.
