# Glossary

Short definitions. Chapters contain the mechanism.

| Term | Definition |
| --- | --- |
| ASGI | Async callable interface between a Python web server and an application. Uvicorn speaks ASGI to FastAPI. |
| Cache validator | `ETag` or `Last-Modified` value a client sends back so the server can answer `304 Not Modified`. |
| Circuit breaker | Client-side or gateway control that stops calling a dependency after repeated failures, then probes for recovery. |
| Correlation ID | Identifier that follows one business operation across services. A request ID identifies a single hop. |
| Cursor / keyset pagination | Page token built from the last seen sort key, not from a numeric offset. |
| HATEOAS | Hypermedia constraint: representations contain links that advertise the next legal transitions. |
| Idempotent | Repeating a completed request has the same effect as doing it once. Safe methods are idempotent; idempotent methods are not all safe. |
| Idempotency-Key | Client-generated key the server stores so a retry of a non-idempotent operation returns the original result. |
| JWT | Signed token with header, payload, and signature. Possession of a valid JWT is not the same as a fresh authorization decision. |
| N+1 query | One query for a collection plus one query per row for a relationship. |
| OAuth 2.0 | Delegated authorization framework. It is not an authentication protocol by itself. |
| OpenID Connect | Identity layer on OAuth 2.0. The ID token asserts an authenticated user. |
| Problem Details | `application/problem+json` error document defined by RFC 9457. |
| RBAC | Authorization from roles assigned to a principal. |
| ABAC | Authorization from attributes of the principal, resource, and environment. |
| BOLA | Broken object-level authorization: an authenticated caller accesses another caller's object by changing an ID. |
| REST | Architectural style with constraints including statelessness, cacheability, and a uniform interface. |
| Safe method | Method that does not request a state change on the server. `GET`, `HEAD`, and `OPTIONS` are safe. |
| SLI / SLO | A measured indicator, and the target for that indicator. |
| SSE | `text/event-stream` response that pushes events down one HTTP response. |
| Starlette | ASGI toolkit FastAPI uses for routing, requests, and responses. |
| Pydantic | Library FastAPI uses to validate and serialize data. This handbook uses Pydantic v2. |
| Uvicorn | ASGI server commonly used to run FastAPI. |
| WSGI | Synchronous Python web server interface used by traditional Flask and Django deployments. |
