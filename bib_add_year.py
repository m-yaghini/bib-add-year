#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

ENTRY_PATTERN = re.compile(r"@(\w+)\s*{\s*([^,]+),", re.MULTILINE)
DATE_PATTERN = re.compile(r"\bdate\s*=\s*[{|\"](\d{4})[-\d]*[}|\"]", re.IGNORECASE)
YEAR_PATTERN = re.compile(r"\byear\s*=", re.IGNORECASE)

def process_bib(content: str) -> str:
    output = []
    entries = re.split(r"(@\w+\s*{[^}]*})", content, flags=re.DOTALL)

    for entry in entries:
        if not entry.strip().startswith("@"):
            output.append(entry)
            continue

        # Check for date field
        m = DATE_PATTERN.search(entry)
        if m:
            year = m.group(1)
            if not YEAR_PATTERN.search(entry):
                # Insert year field just after the date line
                entry = re.sub(
                    r"(date\s*=\s*[{|\"]\d{4}[-\d]*[}|\"]\s*,?)",
                    r"\1\n  year = {" + year + "},",
                    entry,
                    count=1,
                )
        output.append(entry)
    return "".join(output)

def main():
    parser = argparse.ArgumentParser(
        description="Add 'year' field to .bib entries based on 'date'."
    )
    parser.add_argument("input", type=Path, help="Input .bib file")
    parser.add_argument("-o", "--output", type=Path, help="Output file (default: overwrite input)")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    new_text = process_bib(text)

    out_path = args.output if args.output else args.input
    out_path.write_text(new_text, encoding="utf-8")

if __name__ == "__main__":
    main()