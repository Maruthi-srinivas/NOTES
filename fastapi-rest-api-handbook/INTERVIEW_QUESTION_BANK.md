# Interview Question Bank

This file is the consolidated bank. Each chapter also contains its own questions, model answers, incorrect answers, and follow-ups.

Organization: domain, topic ID, difficulty.

The audit pass links every chapter's interview section below. Model answers stay in those chapters. The index is [MASTER_INDEX.md](MASTER_INDEX.md).

## Anchor questions

These are required by the curriculum. Chapters answer them in full. The audit must confirm each one has a model answer.

| Question | Primary chapter |
| --- | --- |
| What happens when an HTTP request reaches a FastAPI application? | [ASGI lifecycle](17_middleware_request_lifecycle/01-asgi-lifecycle-and-middleware.md) |
| Why are GET and PUT different in semantics? | [Method semantics](03_http_methods_status_codes/01-method-semantics.md) |
| How does idempotency help with retries? | [Timeouts and idempotency](08_reliability_resilience/01-timeouts-retries-idempotency.md) |
| What is the difference between 401 and 403? | [Client errors](03_http_methods_status_codes/04-client-error-status-codes.md) |
| How does FastAPI dependency injection work? | [Depends](16_dependency_injection/01-depends-and-scopes.md) |
| How do async endpoints differ from synchronous endpoints? | [Async model](21_async_concurrency/01-asyncio-model.md) |
| Why can blocking code stall an asynchronous application? | [Blocking and offload](21_async_concurrency/02-blocking-and-offload.md) |
| How should database sessions be managed? | [Sessions and queries](22_database_integration/02-transactions-queries-pagination.md) |
| How do middleware and dependencies differ? | [Middleware tradeoffs](17_middleware_request_lifecycle/03-middleware-design-tradeoffs.md) |
| How do you design cursor-based pagination? | [Cursors](06_pagination_filtering_search/02-cursor-and-keyset-pagination.md) |
| How do you prevent BOLA? | [OWASP access risks](10_api_security/01-owasp-api-top-risks.md) |
| How would you implement rate limiting? | [Admission control](08_reliability_resilience/02-circuit-breakers-limits.md) |
| How do you safely process a large file? | [Uploads](23_file_uploads/01-receiving-uploads.md) |
| How would you design a durable background job API? | [Job lifecycle](24_background_jobs/02-job-lifecycle.md) |
| How do you deploy and scale FastAPI? | [Workers](28_scalability_performance/01-process-and-io-model.md) and [containers](30_deployment_operations/01-container-images.md) |
| How would you expose a streaming LLM API? | [LLM surface](31_ai_engineering_integration/01-llm-api-surface.md) |
| How do you debug high p99 latency? | [Measurement](28_scalability_performance/04-measurement-and-saturation.md) |

## By domain

Extracted from chapter section 10. Model answers live in the chapters.

### Domain 1: HTTP and Web Fundamentals

- [Client-Server Architecture and the Request-Response Lifecycle](01_http_web_fundamentals/01-client-server-and-request-lifecycle.md) — section 10 (D01-T01, D01-T02)
- [HTTP, HTTPS, Protocol Versions, and Connection Lifecycle](01_http_web_fundamentals/02-http-versions-and-connections.md) — section 10 (D01-T03, D01-T04, D01-T21, D01-T22)
- [HTTP Message Structure and Body Framing](01_http_web_fundamentals/03-http-message-structure.md) — section 10 (D01-T05, D01-T06, D01-T07, D01-T08, D01-T14)
- [HTTP Methods, Safety, and Idempotence](01_http_web_fundamentals/04-http-methods-safety-idempotence.md) — section 10 (D01-T09, D01-T10)
- [HTTP Status Code Classes](01_http_web_fundamentals/05-status-code-classes.md) — section 10 (D01-T11)
- [Content-Type, Accept, and Content Negotiation](01_http_web_fundamentals/06-content-negotiation.md) — section 10 (D01-T12, D01-T13)
- [Auth Headers, Cookies, Caching, Redirects, and CORS](01_http_web_fundamentals/07-headers-caching-redirects-cors.md) — section 10 (D01-T15, D01-T16, D01-T17, D01-T18, D01-T19, D01-T20)

### Domain 2: REST Architectural Principles

- [REST, HTTP APIs, and Architectural Constraints](02_rest_architecture/01-rest-constraints.md) — section 10 (D02-T01, D02-T02, D02-T03, D02-T04, D02-T05, D02-T06, D02-T07, D02-T08)
- [Resources, Representations, and URI Design](02_rest_architecture/02-resources-and-uris.md) — section 10 (D02-T09, D02-T10, D02-T11, D02-T12, D02-T13)
- [CRUD Mapping, Maturity Model, and HATEOAS](02_rest_architecture/03-crud-maturity-hateoas.md) — section 10 (D02-T14, D02-T15)
- [REST versus RPC, GraphQL, and gRPC](02_rest_architecture/04-rest-vs-rpc-graphql-grpc.md) — section 10 (D02-T16, D02-T17, D02-T18)

### Domain 3: HTTP Methods and Status Codes

- [Method Semantics and Idempotent Design](03_http_methods_status_codes/01-method-semantics.md) — section 10 (D03-T01, D03-T02, D03-T03, D03-T04, D03-T05, D03-T06, D03-T07)
- [Success Status Codes](03_http_methods_status_codes/02-success-status-codes.md) — section 10 (D03-T08, D03-T09, D03-T10, D03-T11)
- [Redirects and 304 Not Modified](03_http_methods_status_codes/03-redirects-and-not-modified.md) — section 10 (D03-T12, D03-T13)
- [Client Error Status Codes](03_http_methods_status_codes/04-client-error-status-codes.md) — section 10 (D03-T14, D03-T15, D03-T16, D03-T17, D03-T18, D03-T19, D03-T20, D03-T21, D03-T22, D03-T23, D03-T24)
- [Server Error Status Codes](03_http_methods_status_codes/05-server-error-status-codes.md) — section 10 (D03-T25, D03-T26, D03-T27, D03-T28)

### Domain 4: REST API Endpoint Design

- [Resource Naming, URLs, and Nesting](04_endpoint_design/01-resource-naming-and-nesting.md) — section 10 (D04-T01, D04-T02, D04-T03, D04-T04, D04-T05, D04-T06)
- [Filtering, Sorting, Pagination, Search, Bulk, and Actions](04_endpoint_design/02-collections-query-and-actions.md) — section 10 (D04-T07, D04-T08, D04-T09, D04-T10, D04-T11, D04-T12, D04-T13)
- [Parameters, Bodies, Representations, and Contracts](04_endpoint_design/03-parameters-bodies-contracts.md) — section 10 (D04-T14, D04-T15, D04-T16, D04-T17, D04-T18)
- [Partial Updates and Resource Lifecycles](04_endpoint_design/04-partial-updates-and-lifecycle.md) — section 10 (D04-T19, D04-T20)
- [Versioning, Compatibility, and Deprecation](04_endpoint_design/05-versioning-and-compatibility.md) — section 10 (D04-T21, D04-T22, D04-T23)

### Domain 5: Request and Response Design

- [JSON, Serialization, and Field Design](05_request_response_design/01-json-validation-and-fields.md) — section 10 (D05-T01, D05-T02, D05-T03, D05-T04, D05-T05, D05-T06, D05-T07, D05-T08)
- [Time, Money, Enums, and Nested Values](05_request_response_design/02-temporal-numeric-and-nested-values.md) — section 10 (D05-T09, D05-T10, D05-T11, D05-T12, D05-T13)
- [File Upload and Download Representations](05_request_response_design/03-file-payloads.md) — section 10 (D05-T14)
- [Error Schemas, Identifiers, and RFC 9457](05_request_response_design/04-error-contracts.md) — section 10 (D05-T15, D05-T16, D05-T17, D05-T18, D05-T19)

### Domain 6: Pagination, Filtering, and Search

- [Offset and Page Pagination](06_pagination_filtering_search/01-offset-and-page-pagination.md) — section 10 (D06-T01, D06-T02, D06-T03)
- [Cursor and Keyset Pagination](06_pagination_filtering_search/02-cursor-and-keyset-pagination.md) — section 10 (D06-T04, D06-T05, D06-T06, D06-T07, D06-T08)
- [Filtering, Sorting, and Search Contracts](06_pagination_filtering_search/03-filtering-sorting-search.md) — section 10 (D06-T09, D06-T10, D06-T11, D06-T12, D06-T13)
- [Index Design, Pagination Cost, and Query Security](06_pagination_filtering_search/04-query-performance-and-security.md) — section 10 (D06-T14, D06-T15, D06-T16)

### Domain 7: Authentication and Authorization

- [Authentication Mechanisms](07_authentication_authorization/01-auth-mechanisms.md) — section 10 (D07-T01, D07-T02, D07-T03, D07-T04, D07-T05, D07-T06)
- [JWT, OAuth 2.0, and OpenID Connect](07_authentication_authorization/02-jwt-oauth-oidc.md) — section 10 (D07-T07, D07-T08, D07-T09, D07-T10)
- [RBAC, ABAC, Object Authorization, and Tenancy](07_authentication_authorization/03-authorization-models.md) — section 10 (D07-T11, D07-T12, D07-T13, D07-T14, D07-T15)
- [Password Hashing, Token Lifecycle, and Secrets](07_authentication_authorization/04-secrets-passwords-tokens.md) — section 10 (D07-T16, D07-T17, D07-T18)
- [CSRF, CORS, Policies, and Per-Caller Limits](07_authentication_authorization/05-csrf-cors-policies-limits.md) — section 10 (D07-T19, D07-T20, D07-T21, D07-T22, D07-T23)

### Domain 8: API Reliability and Resilience

- [Timeouts, Retries, and Idempotency Keys](08_reliability_resilience/01-timeouts-retries-idempotency.md) — section 10 (D08-T01, D08-T02, D08-T03, D08-T04, D08-T05, D08-T06)
- [Circuit Breakers, Bulkheads, and Admission Control](08_reliability_resilience/02-circuit-breakers-limits.md) — section 10 (D08-T07, D08-T08, D08-T09, D08-T10, D08-T11, D08-T12)
- [Degradation, Shedding, and Distributed Failures](08_reliability_resilience/03-degradation-and-failure-domains.md) — section 10 (D08-T13, D08-T14, D08-T15, D08-T16, D08-T17)
- [Retry Safety, Cancellation, and SLIs/SLOs](08_reliability_resilience/04-cancellation-and-slo.md) — section 10 (D08-T18, D08-T19, D08-T20)

### Domain 9: Caching and Performance

- [Browser, Proxy, Server, and Redis Caches](09_caching_performance/01-cache-layers.md) — section 10 (D09-T01, D09-T02, D09-T03, D09-T04)
- [Cache Validators, Invalidation, and Compression](09_caching_performance/02-validators-and-invalidation.md) — section 10 (D09-T05, D09-T06, D09-T07, D09-T08, D09-T09, D09-T10)
- [Pools, Queries, N+1, Payload Size, and Streaming](09_caching_performance/03-data-access-performance.md) — section 10 (D09-T11, D09-T12, D09-T13, D09-T14, D09-T15)
- [Latency, Throughput, and Load Testing](09_caching_performance/04-latency-throughput-load.md) — section 10 (D09-T16, D09-T17, D09-T18)

### Domain 10: API Security

- [OWASP API Security Top 10: Access and Consumption](10_api_security/01-owasp-api-top-risks.md) — section 10 (D10-T01, D10-T02, D10-T03, D10-T04, D10-T05, D10-T06)
- [SSRF, Injection, Mass Assignment, and Data Exposure](10_api_security/02-injection-and-data-exposure.md) — section 10 (D10-T07, D10-T08, D10-T09, D10-T10, D10-T11)
- [SQL Injection, Path Traversal, Uploads, Smuggling, and TLS](10_api_security/03-transport-and-file-attacks.md) — section 10 (D10-T12, D10-T13, D10-T14, D10-T15, D10-T16)
- [Headers, Secrets, Audit Logs, and Dependency Scanning](10_api_security/04-headers-secrets-audit-dependencies.md) — section 10 (D10-T17, D10-T18, D10-T19, D10-T20)

### Domain 11: API Documentation and Testing

- [OpenAPI, Docs UIs, and Contract-First Design](11_api_documentation_testing/01-openapi-and-contracts.md) — section 10 (D11-T01, D11-T02, D11-T03, D11-T04)
- [Unit, Integration, Contract Tests, and API Clients](11_api_documentation_testing/02-test-layers-and-clients.md) — section 10 (D11-T05, D11-T06, D11-T07, D11-T08, D11-T09, D11-T10, D11-T11)
- [Negative, Boundary, Load, Compatibility, and Regression Tests](11_api_documentation_testing/03-negative-load-and-regression.md) — section 10 (D11-T12, D11-T13, D11-T14, D11-T15, D11-T16, D11-T17)

### Domain 12: FastAPI Fundamentals

- [FastAPI, ASGI, Starlette, and Pydantic](12_fastapi_fundamentals/01-fastapi-runtime-foundations.md) — section 10 (D12-T01, D12-T02, D12-T03, D12-T04)
- [Creating, Running, and Lifecycling an Application](12_fastapi_fundamentals/02-application-process.md) — section 10 (D12-T05, D12-T06, D12-T07, D12-T08, D12-T09, D12-T10)
- [Swagger UI, ReDoc, and OpenAPI Generation](12_fastapi_fundamentals/03-generated-documentation.md) — section 10 (D12-T11, D12-T12, D12-T13)
- [Project Structure and Configuration](12_fastapi_fundamentals/04-project-layout-and-settings.md) — section 10 (D12-T14, D12-T15, D12-T16)

### Domain 13: Path, Query, and Request Parameters

- [Path and Query Parameters](13_parameters/01-path-query-and-constraints.md) — section 10 (D13-T01, D13-T02, D13-T03, D13-T04, D13-T05, D13-T06, D13-T07, D13-T08, D13-T09, D13-T10, D13-T11)
- [Aliases, Headers, Cookies, and Parameter Models](13_parameters/02-aliases-headers-cookies-models.md) — section 10 (D13-T12, D13-T13, D13-T14, D13-T15, D13-T16, D13-T17)
- [Parameter Validation Errors](13_parameters/03-validation-error-responses.md) — section 10 (D13-T18)

### Domain 14: Request Bodies and Pydantic

- [Models, Nesting, and Field Presence](14_pydantic_request_models/01-models-and-field-design.md) — section 10 (D14-T01, D14-T02, D14-T03, D14-T04, D14-T05, D14-T06, D14-T07, D14-T08)
- [Validators, Constraints, Enums, and Reuse](14_pydantic_request_models/02-validators-constraints-reuse.md) — section 10 (D14-T09, D14-T10, D14-T11, D14-T12, D14-T13, D14-T14, D14-T15, D14-T16)
- [Serialization, Aliases, and Pydantic v2](14_pydantic_request_models/03-serialization-and-v2.md) — section 10 (D14-T17, D14-T18, D14-T19, D14-T20, D14-T21, D14-T22, D14-T23, D14-T24)
- [Settings, Schemas, Strict Mode, and Error Customization](14_pydantic_request_models/04-settings-schema-strictness.md) — section 10 (D14-T25, D14-T26, D14-T27, D14-T28)

### Domain 15: Routing and Application Structure

- [Routers, Prefixes, Tags, and Modular Design](15_routing_architecture/01-routers-and-modules.md) — section 10 (D15-T01, D15-T02, D15-T03, D15-T04, D15-T05, D15-T06, D15-T07)
- [Service, Repository, and Application Factories](15_routing_architecture/02-layers-and-factories.md) — section 10 (D15-T08, D15-T09, D15-T10, D15-T11, D15-T12, D15-T13)
- [Route Names, Conflicts, Versioning, and Exposure](15_routing_architecture/03-route-identity-and-versioning.md) — section 10 (D15-T14, D15-T15, D15-T16, D15-T17)

### Domain 16: Dependency Injection

- [Depends, Nesting, and Request-Scoped Resources](16_dependency_injection/01-depends-and-scopes.md) — section 10 (D16-T01, D16-T02, D16-T03, D16-T04, D16-T05, D16-T06, D16-T07, D16-T08, D16-T09)
- [Yield, Overrides, Levels, and Execution Order](16_dependency_injection/02-yield-overrides-and-order.md) — section 10 (D16-T10, D16-T11, D16-T12, D16-T13, D16-T14, D16-T15, D16-T16)
- [Async Dependencies versus Service Locators](16_dependency_injection/03-async-dependencies-vs-locators.md) — section 10 (D16-T17, D16-T18)

### Domain 17: Request Lifecycle and Middleware

- [ASGI Lifecycle and Middleware Order](17_middleware_request_lifecycle/01-asgi-lifecycle-and-middleware.md) — section 10 (D17-T01, D17-T02, D17-T03, D17-T04, D17-T05)
- [Identity, Timing, Logging, CORS, Hosts, and Exceptions](17_middleware_request_lifecycle/02-operational-middleware.md) — section 10 (D17-T06, D17-T07, D17-T08, D17-T09, D17-T10, D17-T11, D17-T12)
- [Middleware versus Dependencies, Context, and Cost](17_middleware_request_lifecycle/03-middleware-design-tradeoffs.md) — section 10 (D17-T13, D17-T14, D17-T15, D17-T16, D17-T17)

### Domain 18: Response Handling

- [Serialization and Response Classes](18_response_handling/01-response-classes.md) — section 10 (D18-T01, D18-T02, D18-T03, D18-T04, D18-T05, D18-T06, D18-T07, D18-T08, D18-T09, D18-T10)
- [Headers, Cookies, Status, and Field Filtering](18_response_handling/02-headers-cookies-and-filtering.md) — section 10 (D18-T11, D18-T12, D18-T13, D18-T14, D18-T15, D18-T16)
- [Serialization Cost, ORM Safety, and Large Streams](18_response_handling/03-performance-orm-and-streaming.md) — section 10 (D18-T17, D18-T18, D18-T19)

### Domain 19: Error Handling and Validation

- [HTTPException, Validation Errors, and Handlers](19_error_handling/01-exceptions-and-handlers.md) — section 10 (D19-T01, D19-T02, D19-T03, D19-T04, D19-T05, D19-T06, D19-T07)
- [Error Schemas, Status Selection, and Safe Logging](19_error_handling/02-error-contracts-and-leakage.md) — section 10 (D19-T08, D19-T09, D19-T10, D19-T11, D19-T12, D19-T13)
- [Errors in Background and Async Workflows](19_error_handling/03-errors-outside-the-request.md) — section 10 (D19-T14, D19-T15)

### Domain 20: Authentication and Authorization in FastAPI

- [FastAPI Security Schemes](20_fastapi_authentication/01-security-schemes.md) — section 10 (D20-T01, D20-T02, D20-T03, D20-T04, D20-T05)
- [JWT, Password Hashing, and Current User](20_fastapi_authentication/02-jwt-passwords-and-current-user.md) — section 10 (D20-T06, D20-T07, D20-T08, D20-T09, D20-T10)
- [Roles, Scopes, Ownership, Tenancy, Cookies, and OIDC](20_fastapi_authentication/03-authorization-enforcement.md) — section 10 (D20-T11, D20-T12, D20-T13, D20-T14, D20-T15, D20-T16, D20-T17)
- [OpenAPI Security, Auth Tests, and Failure Handling](20_fastapi_authentication/04-openapi-and-auth-tests.md) — section 10 (D20-T18, D20-T19, D20-T20)

### Domain 21: Async Programming and Concurrency

- [Endpoints, the Event Loop, and Awaitables](21_async_concurrency/01-asyncio-model.md) — section 10 (D21-T01, D21-T02, D21-T03, D21-T04, D21-T05)
- [Blocking I/O, Clients, Pools, and CPU Work](21_async_concurrency/02-blocking-and-offload.md) — section 10 (D21-T06, D21-T07, D21-T08, D21-T09, D21-T10, D21-T11, D21-T12)
- [Cancellation, Locks, Pools, and Context Managers](21_async_concurrency/03-cancellation-limits-contexts.md) — section 10 (D21-T13, D21-T14, D21-T15, D21-T16)
- [Background Work, Races, Backpressure, and Cleanup](21_async_concurrency/04-races-backpressure-cleanup.md) — section 10 (D21-T17, D21-T18, D21-T19, D21-T20, D21-T21)

### Domain 22: Database Integration

- [SQLAlchemy, Sessions, and PostgreSQL](22_database_integration/01-sqlalchemy-and-sessions.md) — section 10 (D22-T01, D22-T02, D22-T03, D22-T04, D22-T05, D22-T06, D22-T07)
- [CRUD, Transactions, Loading, and Pagination](22_database_integration/02-transactions-queries-pagination.md) — section 10 (D22-T08, D22-T09, D22-T10, D22-T11, D22-T12, D22-T13, D22-T14, D22-T15, D22-T16)
- [Alembic, Isolation, Errors, Leaks, and Tests](22_database_integration/03-migrations-isolation-and-tests.md) — section 10 (D22-T17, D22-T18, D22-T19, D22-T20, D22-T21, D22-T22, D22-T23)

### Domain 23: File Uploads and Downloads

- [UploadFile, Forms, Limits, and Streaming Uploads](23_file_uploads/01-receiving-uploads.md) — section 10 (D23-T01, D23-T02, D23-T03, D23-T04, D23-T05, D23-T06, D23-T07, D23-T08, D23-T09)
- [Filenames, Downloads, and Response Types](23_file_uploads/02-safe-storage-and-downloads.md) — section 10 (D23-T10, D23-T11, D23-T12, D23-T13, D23-T14)
- [Object Storage, Presigned URLs, and Background Processing](23_file_uploads/03-object-storage-and-workers.md) — section 10 (D23-T15, D23-T16, D23-T17, D23-T18)

### Domain 24: Background Tasks and Long-Running Jobs

- [BackgroundTasks versus External Queues](24_background_jobs/01-backgroundtasks-and-queues.md) — section 10 (D24-T01, D24-T02, D24-T03, D24-T04, D24-T05, D24-T06, D24-T07)
- [Job Status, Retries, Dead Letters, and Cancellation](24_background_jobs/02-job-lifecycle.md) — section 10 (D24-T08, D24-T09, D24-T10, D24-T11, D24-T12, D24-T13, D24-T14, D24-T15)
- [Distributed Workers, Health, and Shutdown](24_background_jobs/03-workers-in-production.md) — section 10 (D24-T16, D24-T17, D24-T18)

### Domain 25: Advanced FastAPI Features

- [Lifespan and Application Resources](25_advanced_fastapi/01-lifespan.md) — section 10 (D25-T01, D25-T02, D25-T03)
- [WebSockets, SSE, Mounts, and Streaming Bodies](25_advanced_fastapi/02-streams-sockets-and-mounts.md) — section 10 (D25-T04, D25-T05, D25-T06, D25-T07, D25-T08, D25-T09, D25-T10, D25-T11, D25-T12, D25-T13)
- [Custom Routes, GraphQL Boundaries, and Health Probes](25_advanced_fastapi/03-custom-routes-and-probes.md) — section 10 (D25-T14, D25-T15, D25-T16, D25-T17, D25-T18)

### Domain 26: Testing FastAPI Applications

- [TestClient, Pytest, and Async Tests](26_fastapi_testing/01-pytest-and-testclient.md) — section 10 (D26-T01, D26-T02, D26-T03, D26-T04, D26-T05, D26-T06)
- [Auth, Database, and External-Service Test Doubles](26_fastapi_testing/02-fixtures-and-mocks.md) — section 10 (D26-T07, D26-T08, D26-T09, D26-T10, D26-T11, D26-T12)
- [Jobs, Uploads, WebSockets, Errors, and OpenAPI](26_fastapi_testing/03-specialized-api-tests.md) — section 10 (D26-T13, D26-T14, D26-T15, D26-T16, D26-T17)
- [Coverage, Load, and Docker-Based Tests](26_fastapi_testing/04-coverage-load-and-docker-tests.md) — section 10 (D26-T18, D26-T19, D26-T20)

### Domain 27: FastAPI Security

- [Validation, AuthZ, CORS, Hosts, TLS, Cookies, and CSRF](27_fastapi_security/01-edge-and-session-controls.md) — section 10 (D27-T01, D27-T02, D27-T03, D27-T04, D27-T05, D27-T06, D27-T07)
- [Injection, SSRF, Uploads, Rate Limits, and Brute Force](27_fastapi_security/02-injection-uploads-and-limits.md) — section 10 (D27-T08, D27-T09, D27-T10, D27-T11, D27-T12, D27-T13)
- [Secrets, Headers, PII, Audit, Scanning, and DB Privileges](27_fastapi_security/03-secrets-logging-and-dependencies.md) — section 10 (D27-T14, D27-T15, D27-T16, D27-T17, D27-T18, D27-T19, D27-T20)

### Domain 28: Performance and Scalability

- [Workers, Async I/O, and Blocking Detection](28_scalability_performance/01-process-and-io-model.md) — section 10 (D28-T01, D28-T02, D28-T03, D28-T04)
- [Pools, Redis, Compression, Streaming, and Concurrency Caps](28_scalability_performance/02-pools-cache-and-payloads.md) — section 10 (D28-T05, D28-T06, D28-T07, D28-T08, D28-T09, D28-T10)
- [Load Balancing, Horizontal Scale, Shutdown, and Memory](28_scalability_performance/03-scaling-and-shutdown.md) — section 10 (D28-T11, D28-T12, D28-T13, D28-T14, D28-T15)
- [Profiling, Benchmarks, Percentiles, and Exhaustion](28_scalability_performance/04-measurement-and-saturation.md) — section 10 (D28-T16, D28-T17, D28-T18, D28-T19, D28-T20, D28-T21)

### Domain 29: Configuration, Logging, and Observability

- [Settings, Environments, and Structured Logs](29_observability/01-settings-and-logs.md) — section 10 (D29-T01, D29-T02, D29-T03, D29-T04, D29-T05, D29-T06)
- [Metrics, Prometheus, Grafana, and OpenTelemetry](29_observability/02-metrics-and-tracing.md) — section 10 (D29-T07, D29-T08, D29-T09, D29-T10, D29-T11, D29-T12)
- [Probes, SLOs, Alerting, Redaction, and Dependencies](29_observability/03-health-slo-and-redaction.md) — section 10 (D29-T13, D29-T14, D29-T15, D29-T16, D29-T17, D29-T18, D29-T19)

### Domain 30: Deployment and Production Operations

- [Docker Images, Compose, and Health Checks](30_deployment_operations/01-container-images.md) — section 10 (D30-T01, D30-T02, D30-T03, D30-T04, D30-T05, D30-T06, D30-T07)
- [Nginx, TLS, Uvicorn, and Migration Timing](30_deployment_operations/02-proxy-server-and-migrations.md) — section 10 (D30-T08, D30-T09, D30-T10, D30-T11, D30-T12)
- [CI/CD, Image Scanning, and Release Strategies](30_deployment_operations/03-delivery-pipelines.md) — section 10 (D30-T13, D30-T14, D30-T15, D30-T16, D30-T17)
- [Kubernetes, Draining, Backups, and Incidents](30_deployment_operations/04-runtime-operations.md) — section 10 (D30-T18, D30-T19, D30-T20, D30-T21, D30-T22)

### Domain 31: FastAPI for AI Engineering

- [LLM Endpoints, Providers, Schemas, and Streaming](31_ai_engineering_integration/01-llm-api-surface.md) — section 10 (D31-T01, D31-T02, D31-T03, D31-T04, D31-T05, D31-T06)
- [Timeouts, Retries, Quotas, Tokens, and Cancellation](31_ai_engineering_integration/02-provider-reliability-and-cost.md) — section 10 (D31-T07, D31-T08, D31-T09, D31-T10)
- [RAG, Ingestion, Background Processing, and Vectors](31_ai_engineering_integration/03-rag-and-ingestion.md) — section 10 (D31-T11, D31-T12, D31-T13, D31-T14)
- [Agents, MCP, Memory, Routing, and Evaluation](31_ai_engineering_integration/04-agents-memory-and-evaluation.md) — section 10 (D31-T15, D31-T16, D31-T17, D31-T18, D31-T19, D31-T20, D31-T21, D31-T22, D31-T23)
- [Tenant Isolation, Quotas, Guardrails, and Cost Observability](31_ai_engineering_integration/05-tenant-guardrails-and-cost.md) — section 10 (D31-T24, D31-T25, D31-T26, D31-T27)

