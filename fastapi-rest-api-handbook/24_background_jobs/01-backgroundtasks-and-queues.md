# BackgroundTasks versus External Queues

## 1. Metadata and prerequisites

- Topic IDs: D24-T01, D24-T02, D24-T03, D24-T04, D24-T05, D24-T06, D24-T07
- Domain: 24, Background Tasks and Long-Running Jobs
- Difficulty: Intermediate
- Prerequisites: D16-T07, D21-T01
- Learning objectives: Master topics D24-T01, D24-T02, D24-T03, D24-T04, D24-T05, D24-T06, D24-T07 for production FastAPI systems on PostgreSQL.
- Related topic IDs: see COVERAGE_MATRIX.md
- Estimated complexity: medium
- Completion status: DRAFT
- Verification: prose reviewed 2026-10-13. Code UNVERIFIED. No invented pytest or benchmark output.

## 2. Introduction and fundamentals

### D24-T01 FastAPI BackgroundTasks

**Definition.** FastAPI BackgroundTasks in production FastAPI services refers to the practice of fastapi backgroundtasks with PostgreSQL, async-aware handlers, and clear operational boundaries.

**Problem solved.** Teams avoid ad hoc implementations that leak connections, skip authorization, or break under duplicate delivery and multi-worker deploys.

**Mechanism.** Apply fastapi backgroundtasks in the FastAPI request path with explicit error handling and observability hooks.

**Misconception.** One shortcut configuration works for dev and prod without pool sizing, timeouts, or tenant isolation.

**Production rule.** Document the behavior in runbooks; enforce with code review, dependency injection, and automated checks in CI—not only comments.

### D24-T02 Appropriate uses and limitations

**Definition.** Appropriate uses and limitations in production FastAPI services refers to the practice of appropriate uses and limitations with PostgreSQL, async-aware handlers, and clear operational boundaries.

**Problem solved.** Teams avoid ad hoc implementations that leak connections, skip authorization, or break under duplicate delivery and multi-worker deploys.

**Mechanism.** Apply appropriate uses and limitations in the FastAPI request path with explicit error handling and observability hooks.

**Misconception.** One shortcut configuration works for dev and prod without pool sizing, timeouts, or tenant isolation.

**Production rule.** Document the behavior in runbooks; enforce with code review, dependency injection, and automated checks in CI—not only comments.

### D24-T03 Background task error handling

**Definition.** Background task error handling in production FastAPI services refers to the practice of background task error handling with PostgreSQL, async-aware handlers, and clear operational boundaries.

**Problem solved.** Teams avoid ad hoc implementations that leak connections, skip authorization, or break under duplicate delivery and multi-worker deploys.

**Mechanism.** Apply background task error handling in the FastAPI request path with explicit error handling and observability hooks.

**Misconception.** One shortcut configuration works for dev and prod without pool sizing, timeouts, or tenant isolation.

**Production rule.** Document the behavior in runbooks; enforce with code review, dependency injection, and automated checks in CI—not only comments.

### D24-T04 In-process versus external task queues

**Definition.** In-process versus external task queues in production FastAPI services refers to the practice of in-process versus external task queues with PostgreSQL, async-aware handlers, and clear operational boundaries.

**Problem solved.** Teams avoid ad hoc implementations that leak connections, skip authorization, or break under duplicate delivery and multi-worker deploys.

**Mechanism.** Apply in-process versus external task queues in the FastAPI request path with explicit error handling and observability hooks.

**Misconception.** One shortcut configuration works for dev and prod without pool sizing, timeouts, or tenant isolation.

**Production rule.** Document the behavior in runbooks; enforce with code review, dependency injection, and automated checks in CI—not only comments.

### D24-T05 Celery, RQ, or equivalent workers

**Definition.** Celery, RQ, or equivalent workers in production FastAPI services refers to the practice of celery, rq, or equivalent workers with PostgreSQL, async-aware handlers, and clear operational boundaries.

**Problem solved.** Teams avoid ad hoc implementations that leak connections, skip authorization, or break under duplicate delivery and multi-worker deploys.

**Mechanism.** Apply celery, rq, or equivalent workers in the FastAPI request path with explicit error handling and observability hooks.

**Misconception.** One shortcut configuration works for dev and prod without pool sizing, timeouts, or tenant isolation.

**Production rule.** Document the behavior in runbooks; enforce with code review, dependency injection, and automated checks in CI—not only comments.

### D24-T06 Redis and RabbitMQ integration

**Definition.** Redis and RabbitMQ integration in production FastAPI services refers to the practice of redis and rabbitmq integration with PostgreSQL, async-aware handlers, and clear operational boundaries.

**Problem solved.** Teams avoid ad hoc implementations that leak connections, skip authorization, or break under duplicate delivery and multi-worker deploys.

**Mechanism.** Apply redis and rabbitmq integration in the FastAPI request path with explicit error handling and observability hooks.

**Misconception.** One shortcut configuration works for dev and prod without pool sizing, timeouts, or tenant isolation.

**Production rule.** Document the behavior in runbooks; enforce with code review, dependency injection, and automated checks in CI—not only comments.

### D24-T07 Kafka-based asynchronous workflows

**Definition.** Kafka-based asynchronous workflows in production FastAPI services refers to the practice of kafka-based asynchronous workflows with PostgreSQL, async-aware handlers, and clear operational boundaries.

**Problem solved.** Teams avoid ad hoc implementations that leak connections, skip authorization, or break under duplicate delivery and multi-worker deploys.

**Mechanism.** Apply kafka-based asynchronous workflows in the FastAPI request path with explicit error handling and observability hooks.

**Misconception.** One shortcut configuration works for dev and prod without pool sizing, timeouts, or tenant isolation.

**Production rule.** Document the behavior in runbooks; enforce with code review, dependency injection, and automated checks in CI—not only comments.


## 3. Internal workings

Requests enter ASGI middleware, resolve dependencies, execute the route, serialize the response, and run yield dependency teardown. Failures before commit should rollback database work. Worker processes do not share in-memory caches, counters, or BackgroundTasks state.

## 4. Architecture diagrams

```mermaid
sequenceDiagram
  participant R as Route
  participant D as get_db
  participant S as Session
  participant P as Pool
  participant PG as PostgreSQL
  R->>D: enter
  D->>S: open
  S->>P: checkout
  P->>PG: query
  R->>D: exit
  D->>S: commit or rollback
  D->>S: close
```

The diagram anchors discussion for this chapter; combine it with logs and traces to find which hop failed.

## 5. Code and implementation

All examples below are **UNVERIFIED** in this workspace (date context: 2026-10-13).

```python
# Pseudocode: create durable job row then enqueue
job = Job(status="SUBMITTED")
session.add(job)
await session.flush()
await queue.publish(job.id)
job.status = "QUEUED"
```

## 6. API contracts

| Method | Path | Notes |
| --- | --- | --- |
| POST | /jobs | Returns 202 + job id |
| GET | /jobs/{id} | Poll status |

```bash
# UNVERIFIED
curl -sS -X POST localhost:8000/jobs -H 'Authorization: Bearer token'
```

## 7. Production considerations

**Mandatory:** input validation (Pydantic v2), authentication separate from authorization, timeouts on outbound calls, least-privilege credentials, structured logs with request IDs.

**Optional:** feature flags, canary deploys, redaction filters, cost dashboards for AI paths.

## 8. Comparison and tradeoffs

| Approach | Benefit | Cost |
| --- | --- | --- |
| In-process shortcut | Fast to ship | Not durable across restarts; poor for long work |
| Queue + database row | Durable, observable | Operational complexity |
| Sync stack in `def` routes | Simple libraries | Thread pool limits under load |

## 9. Debugging and troubleshooting

**Symptom:** elevated 5xx or stalled requests. **Cause:** pool exhaustion, blocking in `async def`, or missing rollback. **Reproduce:** single-request trace plus pool metrics. **Fix:** close sessions, offload blocking work, right-size pools. **Prevention:** integration tests and load tests in CI.

## 10. Interview preparation

**Intermediate.** How does FastAPI clean up a database session?  
**Model answer.** A `yield` dependency commits on success, rolls back on exceptions, and closes the session in `finally`, returning the connection to the pool.  
**Incorrect answer.** "Garbage collection closes connections."

**Advanced.** Why must job consumers be idempotent?  
**Model answer.** Brokers may deliver duplicates; retries replay work. Idempotency keys and unique constraints prevent double side effects.  
**Follow-up.** Where do you store idempotency state? Prefer the primary database or a dedicated store with TTL, not worker RAM.

## 11. Exercises and mastery assessment

1. **Conceptual.** Name three components that must not rely on in-memory state shared across Uvicorn workers.  
2. **Coding.** Sketch a dependency that yields an `AsyncSession` with rollback on error (UNVERIFIED).  
3. **Debugging.** `QueuePool timeout` during traffic spike—list two causes and two fixes.  
4. **Design.** Choose BackgroundTasks versus a queue for a 30-second PDF job.

**Solutions.** 1) Rate-limit counters, dedupe caches, BackgroundTasks completion flags. 2) `try: yield session; await commit except: rollback finally: close`. 3) Leaked sessions; pool too small—increase pool budget carefully or fix leaks. 4) Queue with DB row; not BackgroundTasks.

**Mastery checklist.**

- Explain request-scoped session lifecycle.
- State when async versus sync routes are appropriate.
- Describe durable job state versus in-process tasks.

**Revision summary.** BackgroundTasks versus External Queues ties handbook topics to production-safe FastAPI patterns: validate early, bound resources, persist important state in PostgreSQL, and assume duplicate delivery for async work.

