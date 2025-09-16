#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

# Regex to match date field, e.g. date = {2023-11-02} or date = "2023"
DATE_FIELD = re.compile(
    r"(?P<prefix>\bdate\s*=\s*[{\"]\s*)(?P<year>\d{4})(?:[-\d]*)?(?P<suffix>\s*[}\"])",
    re.IGNORECASE,
)

# Regex to detect an existing year field
YEAR_FIELD = re.compile(r"\byear\s*=", re.IGNORECASE)


def add_year_to_entry(entry: str) -> str:
    """If entry has a date but no year, inject a year field."""
    if YEAR_FIELD.search(entry):
        return entry  # already has a year

    m = DATE_FIELD.search(entry)
    if not m:
        return entry  # no date found

    year = m.group("year")

    # Where to insert the year line:
    # insert after the matched date line
    lines = entry.splitlines()
    for i, line in enumerate(lines):
        if "date" in line.lower():
            indent = re.match(r"^\s*", line).group(0)  # preserve indentation
            lines.insert(i + 1, f"{indent}year = {{{year}}},")
            break
    return "\n".join(lines)


def process_bib(text: str) -> str:
    # Split into entries starting with "@"
    parts = re.split(r"(?=@\w+\s*{)", text, flags=re.MULTILINE)
    processed = [add_year_to_entry(p) if p.strip().startswith("@") else p for p in parts]
    return "".join(processed)


def main():
    parser = argparse.ArgumentParser(
        description="Add 'year' field to .bib entries based on 'date'."
    )
    parser.add_argument("input", type=Path, help="Input .bib file")
    parser.add_argument(
        "-o", "--output", type=Path, help="Output file (default: overwrite input)"
    )
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    new_text = process_bib(text)

    out_path = args.output if args.output else args.input
    out_path.write_text(new_text, encoding="utf-8")


if __name__ == "__main__":
    main()