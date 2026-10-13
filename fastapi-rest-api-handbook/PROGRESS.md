# Progress

- Current generation batch: 8 (audit)
- Next topic ID: none in the inventory. Resume work is verification, not a missing topic.
- Chapter status: all 619 subtopics are `TECHNICALLY_REVIEWED`
- Project status: source and Docker files exist; pytest has not been executed

## Status legend

NOT_STARTED, OUTLINED, DRAFTED, TECHNICALLY_REVIEWED, TESTED, COMPLETE

No topic is marked `COMPLETE` or `TESTED`. Completion requires an executed test or a recorded run. Those runs have not happened.

## Files created

- Tracking files at the handbook root
- 118 chapter files under domains 01–31
- Three projects under `projects/`

## Validation results

- `_meta/curriculum.py` asserts every subtopic appears in exactly one chapter. Result: 31 domains, 619 subtopics, 118 chapters.
- After the remaining domain chapters landed, coverage was checked again: all 118 chapters still have sections 1, 2, 3, 10, and 11 and every assigned topic ID.
- Relative Markdown links: 1558 checked, 0 missing.
- Docker daemon was not running (`npipe:////./pipe/dockerDesktopLinuxEngine` was missing). Project pytest was not executed. Chapter snippets were not executed.
- Standards review date recorded in chapters: 2026-10-13.

## Unresolved issues

- Start Docker Desktop, then from each project directory run `docker compose run --rm api pytest`.
- Replace ecommerce `create_all` with Alembic before treating Project A as a migration pipeline.
- Project B can leave a `QUEUED` row without a Redis message if the process dies after commit and before `LPUSH`, and a `RUNNING` row can stick if the worker dies. Both need a sweeper before production.
- Project C uses a shared demo password and an HTTP stand-in for MCP, not the official MCP SDK.
- Library pins in the project `requirements.txt` files were not installed or import-checked in this environment.

## Counts

- Domains: 31
- Subtopics: 619
- Chapters: 118
- Projects: 3
