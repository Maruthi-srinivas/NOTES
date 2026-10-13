"""Generate handbook navigation files from curriculum.py."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_meta"))

from curriculum import CHAPTERS, DOMAINS, chapter_for, iter_topics, topic_id  # noqa: E402

PROJECTS = [
    ("projects/ecommerce_rest_api/", "Project A: E-commerce REST API"),
    ("projects/asynchronous_job_api/", "Project B: Asynchronous Job Processing API"),
    ("projects/production_ai_api/", "Project C: Production AI API"),
]


def write(relative: str, text: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def checklist() -> str:
    topics = list(iter_topics())
    chapter_count = sum(len(items) for items in CHAPTERS.values())
    lines = [
        "# Master Checklist",
        "",
        "Stable inventory for the REST API and FastAPI handbook.",
        "",
        f"- Domains: {len(DOMAINS)}",
        f"- Subtopics: {len(topics)}",
        f"- Chapters: {chapter_count}",
        "- Projects: 3",
        "",
        "Status values: `NOT_STARTED`, `OUTLINED`, `DRAFTED`, `TECHNICALLY_REVIEWED`, `TESTED`, `COMPLETE`.",
        "",
        "A topic is not complete because a heading exists. `COMPLETE` requires the chapter section, an implementation or an explicit not-applicable reason, a test or a documented verification gap, exercises, and an interview answer.",
        "",
    ]
    for domain, (title, folder, names) in DOMAINS.items():
        lines.append(f"## Domain {domain}: {title}")
        lines.append("")
        lines.append(f"Directory: [{folder}]({folder}/)")
        lines.append("")
        lines.append("| Topic ID | Title | Chapter | Status |")
        lines.append("| --- | --- | --- | --- |")
        for index, name in enumerate(names, start=1):
            rel, _chapter_title, _difficulty = chapter_for(domain, index)
            tid = topic_id(domain, index)
            lines.append(f"| {tid} | {name} | [{rel}]({rel}) | NOT_STARTED |")
        lines.append("")
    lines.append("## Projects")
    lines.append("")
    for path, title in PROJECTS:
        lines.append(f"- NOT_STARTED: [{title}]({path})")
    lines.append("")
    return "\n".join(lines)


def coverage() -> str:
    lines = [
        "# Coverage Matrix",
        "",
        "One row per subtopic. Update statuses in place. Do not delete rows.",
        "",
        "| Topic ID | Topic title | Chapter file | Explanation | Implementation | Tests | Exercises | Interview | Technical review | Verification |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for domain, index, tid, name in iter_topics():
        rel, _title, _difficulty = chapter_for(domain, index)
        lines.append(
            f"| {tid} | {name} | [{rel}]({rel}) | NOT_STARTED | NOT_STARTED | NOT_STARTED | NOT_STARTED | NOT_STARTED | NOT_STARTED | NOT_STARTED |"
        )
    lines.append("")
    lines.append("## Projects")
    lines.append("")
    lines.append("| Project | Path | Status | Tests | Docker | Security review |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for path, title in PROJECTS:
        lines.append(f"| {title} | [{path}]({path}) | NOT_STARTED | NOT_STARTED | NOT_STARTED | NOT_STARTED |")
    lines.append("")
    return "\n".join(lines)


def index() -> str:
    lines = [
        "# Master Index",
        "",
        "Offline navigation for the handbook. Links are relative.",
        "",
        "## Start here",
        "",
        "- [README](README.md)",
        "- [Master checklist](MASTER_CHECKLIST.md)",
        "- [Coverage matrix](COVERAGE_MATRIX.md)",
        "- [Dependency graph](DEPENDENCY_GRAPH.md)",
        "- [Progress](PROGRESS.md)",
        "- [Glossary](GLOSSARY.md)",
        "- [Interview question bank](INTERVIEW_QUESTION_BANK.md)",
        "- [Flashcards](FLASHCARDS.md)",
        "- [References](REFERENCES.md)",
        "- [Chapter template](CHAPTER_TEMPLATE.md)",
        "",
        "## Study order",
        "",
        "Read domains 1 through 31 in order, then the projects. Prerequisite edges are in the dependency graph.",
        "",
        "## Chapters",
        "",
    ]
    for domain, (title, folder, _names) in DOMAINS.items():
        lines.append(f"### Domain {domain}: {title}")
        lines.append("")
        for filename, chapter_title, difficulty, numbers in CHAPTERS[domain]:
            ids = ", ".join(topic_id(domain, number) for number in numbers)
            lines.append(
                f"- [{chapter_title}]({folder}/{filename}) ({difficulty}; {ids})"
            )
        lines.append("")
    lines.append("## Projects")
    lines.append("")
    for path, title in PROJECTS:
        lines.append(f"- [{title}]({path}README.md)")
    lines.append("")
    lines.append("## Interview and exercises")
    lines.append("")
    lines.append("Each chapter contains interview questions and exercises. The consolidated bank is [INTERVIEW_QUESTION_BANK.md](INTERVIEW_QUESTION_BANK.md).")
    lines.append("")
    return "\n".join(lines)


def dependency() -> str:
    return """# Dependency Graph

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
"""


def progress() -> str:
    topics = list(iter_topics())
    chapter_count = sum(len(items) for items in CHAPTERS.values())
    return f"""# Progress

- Current generation batch: 0 (scaffold)
- Next topic ID: D01-T01
- Completed topics: 0
- In-progress topics: none
- Pending topics: {len(topics)} subtopics, {chapter_count} chapters, 3 projects

## Status legend

NOT_STARTED, OUTLINED, DRAFTED, TECHNICALLY_REVIEWED, TESTED, COMPLETE

## Files created

Scaffold and tracking files only. Chapter bodies are not written in this batch.

## Validation results

- Curriculum map self-check: every subtopic is assigned to exactly one chapter.
- Executed tests: none yet.
- Examples: none yet. Future unexecuted examples must be marked unverified.

## Unresolved issues

- No chapter prose has been technically reviewed yet.
- Docker execution has not been run.

## Counts

- Domains: {len(DOMAINS)}
- Subtopics: {len(topics)}
- Chapters: {chapter_count}
- Projects: 3
"""


def main() -> None:
    for _domain, (_title, folder, _names) in DOMAINS.items():
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    for path, _title in PROJECTS:
        (ROOT / path).mkdir(parents=True, exist_ok=True)
    write("MASTER_CHECKLIST.md", checklist())
    write("COVERAGE_MATRIX.md", coverage())
    write("MASTER_INDEX.md", index())
    write("DEPENDENCY_GRAPH.md", dependency())
    write("PROGRESS.md", progress())
    print(f"domains={len(DOMAINS)} topics={sum(len(v[2]) for v in DOMAINS.values())} chapters={sum(len(v) for v in CHAPTERS.values())}")


if __name__ == "__main__":
    main()
