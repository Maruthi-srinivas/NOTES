"""Mark Domain 1 rows as technically reviewed."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    checklist = ROOT / "MASTER_CHECKLIST.md"
    lines = []
    for line in checklist.read_text(encoding="utf-8").splitlines():
        if line.startswith("| D01-"):
            line = line.replace("| NOT_STARTED |", "| TECHNICALLY_REVIEWED |")
        lines.append(line)
    checklist.write_text("\n".join(lines) + "\n", encoding="utf-8")

    matrix = ROOT / "COVERAGE_MATRIX.md"
    updated = []
    for line in matrix.read_text(encoding="utf-8").splitlines():
        if line.startswith("| D01-"):
            parts = line.split("|")
            parts[4] = " TECHNICALLY_REVIEWED "
            parts[5] = " ILLUSTRATIVE_UNVERIFIED "
            parts[6] = " NOT_APPLICABLE "
            parts[7] = " COMPLETE "
            parts[8] = " COMPLETE "
            parts[9] = " TECHNICALLY_REVIEWED "
            parts[10] = " UNVERIFIED_NO_EXECUTION "
            line = "|".join(parts)
        updated.append(line)
    matrix.write_text("\n".join(updated) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
