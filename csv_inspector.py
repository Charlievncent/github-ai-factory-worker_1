"""Analyze CSV files and report useful data-quality statistics."""

import argparse
import csv
import json
import sys
from collections import Counter


def analyze_csv(file_path):
    """Return row count, columns, missing values and duplicate count."""
    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        try:
            columns = next(reader)
        except StopIteration:
            raise ValueError("CSV file is empty")

        if not columns:
            raise ValueError("CSV header is empty")

        missing = Counter()
        seen = set()
        duplicates = 0
        rows = 0

        for row in reader:
            if not row:
                continue

            rows += 1
            normalized = tuple(row)

            if normalized in seen:
                duplicates += 1
            else:
                seen.add(normalized)

            for index, column in enumerate(columns):
                value = row[index] if index < len(row) else ""
                if not value.strip():
                    missing[column] += 1

        return {
            "rows": rows,
            "columns": columns,
            "missing_values": {
                column: missing[column] for column in columns
            },
            "duplicate_rows": duplicates
        }


def main():
    parser = argparse.ArgumentParser(description="Inspect a CSV file.")
    parser.add_argument("file", help="Path to CSV file")
    args = parser.parse_args()

    try:
        print(json.dumps(analyze_csv(args.file), indent=2))
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
