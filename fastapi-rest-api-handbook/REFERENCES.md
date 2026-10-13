# References

Checked on 2026-10-13. Prefer these sources over blog posts when they disagree. Version-sensitive library behavior still has to be checked against the release you pin.

## HTTP and API standards

- RFC 9110, HTTP Semantics: https://www.rfc-editor.org/rfc/rfc9110
- RFC 9111, HTTP Caching: https://www.rfc-editor.org/rfc/rfc9111
- RFC 9112, HTTP/1.1: https://www.rfc-editor.org/rfc/rfc9112
- RFC 9113, HTTP/2: https://www.rfc-editor.org/rfc/rfc9113
- RFC 9114, HTTP/3: https://www.rfc-editor.org/rfc/rfc9114
- RFC 9457, Problem Details for HTTP APIs: https://www.rfc-editor.org/rfc/rfc9457
- RFC 9209, The Origin HTTP Header: https://www.rfc-editor.org/rfc/rfc9209 (related to DNS rebinding and origin checks; not a substitute for application authorization)
- RFC 7519, JSON Web Token: https://www.rfc-editor.org/rfc/rfc7519
- RFC 6749, The OAuth 2.0 Authorization Framework: https://www.rfc-editor.org/rfc/rfc6749
- OpenID Connect Core: https://openid.net/specs/openid-connect-core-1_0.html
- Fetch standard, CORS: https://fetch.spec.whatwg.org/
- OpenAPI Specification 3.1: https://spec.openapis.org/oas/v3.1.0
- Richardson Maturity Model (Leonard Richardson, popularized by Martin Fowler): https://martinfowler.com/articles/richardsonMaturityModel.html
- Fielding, Architectural Styles and the Design of Network-based Software Architectures, 2000

## Security

- OWASP API Security Top 10 (2023): https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/

## Python stack

- Python documentation: https://docs.python.org/3/
- FastAPI documentation: https://fastapi.tiangolo.com/
- Starlette documentation: https://www.starlette.io/
- Pydantic v2 documentation: https://docs.pydantic.dev/latest/
- Uvicorn documentation: https://www.uvicorn.org/
- SQLAlchemy 2.0 documentation: https://docs.sqlalchemy.org/en/20/
- Alembic documentation: https://alembic.sqlalchemy.org/
- PostgreSQL documentation: https://www.postgresql.org/docs/current/
- pytest documentation: https://docs.pytest.org/

## Operations

- Docker documentation: https://docs.docker.com/
- OpenTelemetry documentation: https://opentelemetry.io/docs/
- Prometheus documentation: https://prometheus.io/docs/

## Uncertainty

Library tutorials move. When a chapter names `pwdlib`, Pydantic Settings, or SQLAlchemy `async_sessionmaker`, the chapter records that the example was or was not executed. If an API in a chapter disagrees with the current official page, trust the official page and update the chapter.
