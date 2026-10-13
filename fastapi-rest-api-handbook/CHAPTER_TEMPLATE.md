# Chapter Template

Copy this structure for every chapter. Delete a section only when it is genuinely not applicable, and say why.

```markdown
# Title

## 1. Metadata and prerequisites

- Topic IDs:
- Domain:
- Difficulty:
- Prerequisites:
- Learning objectives:
- Related topic IDs:
- Estimated complexity:
- Completion status:

## 2. Introduction and fundamentals

Formal definition, intuition, the problem solved, terminology, use cases, and misconceptions.

## 3. Internal workings

Step-by-step mechanism. Protocol path, framework path, or attack path as appropriate.

## 4. Architecture diagrams

Mermaid, then prose that explains the diagram.

## 5. Code and implementation

File names, commands, expected behavior. Mark unverified examples. Separate pseudocode from executable code.

## 6. API contracts

Method, path, parameters, headers, auth, schemas, status codes, idempotency. Include curl when an endpoint exists.

## 7. Production considerations

Mandatory controls versus optional enhancements.

## 8. Comparison and tradeoffs

Context-specific comparison. No universal winner.

## 9. Debugging and troubleshooting

Symptom, cause, reproduction, diagnosis, fix, prevention, tests.

## 10. Interview preparation

Question, difficulty, model answer, common incorrect answer, follow-up.

## 11. Exercises and mastery assessment

Conceptual, coding, debugging, design, production. Hints, solutions, verification criteria, mastery checklist, revision summary.
```

## Writing rules

- Use topic IDs from `_meta/curriculum.py` exactly.
- Cite RFC 9110 for HTTP semantics, RFC 9112 for HTTP/1.1 messaging, RFC 9113 for HTTP/2, RFC 9114 for HTTP/3, RFC 9111 for caching, and RFC 9457 for problem details.
- Pydantic examples use v2 APIs (`model_validate`, `model_dump`, `field_validator`).
- Do not invent benchmark numbers or test output.
- Do not put secrets in examples. Use placeholders such as `change-me`.
- State that worker processes do not share in-memory caches, counters, sessions, or background tasks.
- Keep authentication and authorization as separate checks.
