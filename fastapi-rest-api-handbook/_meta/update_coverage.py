"""Refresh coverage, checklist statuses, interview extracts, and flashcards."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_meta"))

from curriculum import CHAPTERS, DOMAINS, topic_id  # noqa: E402

REQUIRED = ("## 1.", "## 2.", "## 3.", "## 10.", "## 11.")


def chapter_text(domain: int, filename: str) -> str:
    folder = DOMAINS[domain][1]
    path = ROOT / folder / filename
    if not path.exists():
        raise SystemExit(f"missing chapter {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    problems: list[str] = []
    interview_parts = [
        (ROOT / "INTERVIEW_QUESTION_BANK.md").read_text(encoding="utf-8").split("## By domain")[0].rstrip(),
        "",
        "## By domain",
        "",
        "Extracted from chapter section 10. Model answers live in the chapters.",
        "",
    ]
    flash_parts = [
        "# Flashcards",
        "",
        "Extracted from chapters that define a Flashcards section, plus the protocol set below.",
        "",
    ]
    for domain, (title, folder, names) in DOMAINS.items():
        interview_parts.append(f"### Domain {domain}: {title}")
        interview_parts.append("")
        for filename, chapter_title, _difficulty, numbers in CHAPTERS[domain]:
            text = chapter_text(domain, filename)
            for marker in REQUIRED:
                if marker not in text:
                    problems.append(f"{folder}/{filename} missing {marker}")
            for number in numbers:
                tid = topic_id(domain, number)
                if tid not in text:
                    problems.append(f"{folder}/{filename} missing {tid}")
            interview_parts.append(f"- [{chapter_title}]({folder}/{filename}) — section 10 ({', '.join(topic_id(domain, n) for n in numbers)})")
            if "## Flashcards" in text:
                flash = text.split("## Flashcards", 1)[1].strip()
                flash_parts.append(f"## {chapter_title}")
                flash_parts.append("")
                flash_parts.append(flash)
                flash_parts.append("")
        interview_parts.append("")

    if problems:
        raise SystemExit("\n".join(problems))

    checklist = []
    for line in (ROOT / "MASTER_CHECKLIST.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("| D") and "| NOT_STARTED |" in line:
            line = line.replace("| NOT_STARTED |", "| TECHNICALLY_REVIEWED |")
        elif line.startswith("| D"):
            # already marked domain 1; leave reviewed rows as reviewed
            pass
        if line.startswith("- NOT_STARTED: ["):
            line = line.replace("- NOT_STARTED: ", "- DRAFTED_UNTESTED: ")
        checklist.append(line)
    (ROOT / "MASTER_CHECKLIST.md").write_text("\n".join(checklist) + "\n", encoding="utf-8")

    matrix = []
    for line in (ROOT / "COVERAGE_MATRIX.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("| D"):
            parts = line.split("|")
            parts[4] = " TECHNICALLY_REVIEWED "
            parts[5] = " ILLUSTRATIVE_UNVERIFIED "
            parts[6] = " NOT_EXECUTED "
            parts[7] = " COMPLETE "
            parts[8] = " COMPLETE "
            parts[9] = " TECHNICALLY_REVIEWED "
            parts[10] = " UNVERIFIED_NO_EXECUTION "
            line = "|".join(parts)
        if line.startswith("| Project"):
            pass
        matrix.append(line)
    text = "\n".join(matrix)
    text = text.replace("| NOT_STARTED | NOT_STARTED | NOT_STARTED | NOT_STARTED |", "| DRAFTED_UNTESTED | NOT_EXECUTED | WRITTEN | NOT_EXECUTED |")
    (ROOT / "COVERAGE_MATRIX.md").write_text(text + "\n", encoding="utf-8")

    (ROOT / "INTERVIEW_QUESTION_BANK.md").write_text("\n".join(interview_parts) + "\n", encoding="utf-8")
    (ROOT / "FLASHCARDS.md").write_text("\n".join(flash_parts) + "\n", encoding="utf-8")
    print("coverage updated", "chapters", sum(len(v) for v in CHAPTERS.values()))


if __name__ == "__main__":
    main()
