# REST API and FastAPI Engineering Handbook

This handbook trains a computer science graduate to design, implement, test, debug, secure, document, deploy, and operate production HTTP APIs with Python and FastAPI.

It is an offline knowledge base. Start with [MASTER_INDEX.md](MASTER_INDEX.md). The authoritative topic list is [MASTER_CHECKLIST.md](MASTER_CHECKLIST.md). Study order and prerequisites are in [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md).

## How to study

1. Read the domain in order. Each chapter names its topic IDs.
2. Trace the diagram before reading the code.
3. Treat illustrative snippets as explanations. Treat a block marked runnable as something you can execute.
4. Examples that were not executed in a container are marked **unverified**.
5. Do the exercises before reading the solutions.
6. After domains 1–30, build the projects under [projects/](projects/).

## What this handbook will not pretend

- An HTTP API is not automatically a REST API.
- Authentication is not authorization.
- `OAuth2PasswordBearer` extracts a bearer token and documents a security scheme. It is not an OAuth authorization server.
- `BackgroundTasks` does not survive process death. Durable work needs an external queue and a persisted job record.
- Uvicorn worker processes do not share ordinary Python memory.
- Model output is untrusted input.

## Runnable work

Substantial projects use Docker Compose. Do not install project dependencies on the host. Commands for each project are in that project's `README.md`.

Shared lab notes live next to the chapter that needs them. Small protocol examples use `curl` illustrations and are not separate applications.

## Tracking

| File | Role |
| --- | --- |
| [MASTER_CHECKLIST.md](MASTER_CHECKLIST.md) | Every domain, subtopic, and topic ID |
| [COVERAGE_MATRIX.md](COVERAGE_MATRIX.md) | Explanation, implementation, tests, exercises, interview, review |
| [PROGRESS.md](PROGRESS.md) | Batch, next topic, validation gaps |
| [GLOSSARY.md](GLOSSARY.md) | Short definitions |
| [INTERVIEW_QUESTION_BANK.md](INTERVIEW_QUESTION_BANK.md) | Questions consolidated from chapters |
| [FLASHCARDS.md](FLASHCARDS.md) | Recall prompts |
| [REFERENCES.md](REFERENCES.md) | Standards and official docs |

Verification date for standards cited throughout: 2026-10-13. Re-check version-sensitive FastAPI, Pydantic, SQLAlchemy, and Uvicorn behavior against current official docs before production use.
