# Dependency Graph

Recommended study order follows the domain numbers. Edges below are prerequisites, not the only useful reading order.

```mermaid
flowchart TD
  d01[D01_HTTP]
  d02[D02_REST]
  d03[D03_Methods_Status]
  d04[D04_Endpoints]
  d05[D05_Payloads]
  d06[D06_Pagination]
  d07[D07_Auth_Design]
  d08[D08_Reliability]
  d09[D09_Caching]
  d10[D10_API_Security]
  d11[D11_Docs_Tests]
  d12[D12_FastAPI]
  d13[D13_Parameters]
  d14[D14_Pydantic]
  d15[D15_Routing]
  d16[D16_Dependencies]
  d17[D17_Middleware]
  d18[D18_Responses]
  d19[D19_Errors]
  d20[D20_FastAPI_Auth]
  d21[D21_Async]
  d22[D22_Database]
  d23[D23_Files]
  d24[D24_Jobs]
  d25[D25_Advanced]
  d26[D26_Testing]
  d27[D27_FastAPI_Security]
  d28[D28_Scale]
  d29[D29_Observability]
  d30[D30_Deploy]
  d31[D31_AI]
  projA[ProjectA_Ecommerce]
  projB[ProjectB_Jobs]
  projC[ProjectC_AI]
  d01 --> d02 --> d03 --> d04 --> d05 --> d06
  d03 --> d07
  d01 --> d08
  d01 --> d09
  d07 --> d10
  d05 --> d11
  d02 --> d12
  d12 --> d13 --> d14 --> d15 --> d16 --> d17 --> d18 --> d19
  d07 --> d20
  d16 --> d20
  d12 --> d21
  d21 --> d22
  d16 --> d22
  d18 --> d23
  d21 --> d24
  d22 --> d24
  d17 --> d25
  d19 --> d26
  d22 --> d26
  d10 --> d27
  d20 --> d27
  d21 --> d28
  d22 --> d28
  d08 --> d29
  d28 --> d30
  d29 --> d30
  d21 --> d31
  d24 --> d31
  d06 --> projA
  d20 --> projA
  d22 --> projA
  d24 --> projB
  d29 --> projB
  d31 --> projC
  d27 --> projC
  d30 --> projA
  d30 --> projB
  d30 --> projC
```

## Prerequisite rules

- Domains 1–3 before endpoint and payload design.
- Domains 4–6 before pagination-heavy project work.
- Domain 7 before FastAPI authentication in Domain 20.
- Domains 12–19 before database, jobs, and testing chapters that assume those mechanics.
- Domain 21 before async SQLAlchemy, streaming, and model-provider calls.
- Domains 22 and 24 before Projects A and B.
- Domains 27–30 before treating a project as production-ready.
- Domain 31 before Project C.

## Cross-links that must stay distinct

- Domain 1 explains protocol mechanics. Domain 3 explains which method and status an API should choose.
- Domain 7 explains authentication and authorization design. Domain 20 shows FastAPI security utilities. Domain 27 applies those controls in a production configuration.
- Domain 9 explains caching and performance concepts. Domain 28 explains process model, saturation, and scaling.
- Domain 11 explains the test taxonomy. Domain 26 shows FastAPI and pytest mechanics.
