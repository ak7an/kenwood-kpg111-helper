#!/usr/bin/env python3
"""Validate Talk Group and Individual ID CSV files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_COLUMNS = ("type", "name", "id")
VALID_TYPES = {"TG", "INDIVIDUAL"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate CSV files with columns: type,name,id"
    )
    parser.add_argument("csv_files", nargs="+", type=Path, help="CSV file(s) to validate")
    parser.add_argument(
        "--unique-ids",
        action="store_true",
        help="Report duplicate IDs within each type across all supplied CSV files",
    )
    parser.add_argument(
        "--unique-names",
        action="store_true",
        help="Report duplicate names within each type across all supplied CSV files",
    )
    return parser.parse_args()


def validate_header(path: Path, fieldnames: list[str] | None) -> list[str]:
    errors = []
    if fieldnames is None:
        return [f"{path}: missing CSV header"]

    missing = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
    if missing:
        errors.append(f"{path}: missing required column(s): {', '.join(missing)}")

    extra = [column for column in fieldnames if column not in REQUIRED_COLUMNS]
    if extra:
        errors.append(f"{path}: unexpected column(s): {', '.join(extra)}")

    if fieldnames[: len(REQUIRED_COLUMNS)] != list(REQUIRED_COLUMNS):
        errors.append(f"{path}: header must start with: {','.join(REQUIRED_COLUMNS)}")

    return errors


def parse_id(value: str) -> int | None:
    stripped = value.strip()
    if not stripped.isdecimal():
        return None
    parsed = int(stripped, 10)
    if parsed <= 0:
        return None
    return parsed


def validate_file(path: Path) -> tuple[list[str], list[tuple[str, str, int, Path, int]]]:
    errors = []
    rows = []

    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            errors.extend(validate_header(path, reader.fieldnames))
            if errors:
                return errors, rows

            for line_number, row in enumerate(reader, start=2):
                raw_type = (row.get("type") or "").strip()
                raw_name = (row.get("name") or "").strip()
                raw_id = (row.get("id") or "").strip()

                if raw_type not in VALID_TYPES:
                    errors.append(
                        f"{path}:{line_number}: type must be TG or INDIVIDUAL, got {raw_type!r}"
                    )
                if not raw_name:
                    errors.append(f"{path}:{line_number}: name must not be blank")

                parsed_id = parse_id(raw_id)
                if parsed_id is None:
                    errors.append(
                        f"{path}:{line_number}: id must be a positive decimal integer, got {raw_id!r}"
                    )

                if raw_type in VALID_TYPES and raw_name and parsed_id is not None:
                    rows.append((raw_type, raw_name, parsed_id, path, line_number))
    except FileNotFoundError:
        errors.append(f"{path}: file not found")
    except OSError as exc:
        errors.append(f"{path}: could not read file: {exc}")
    except csv.Error as exc:
        errors.append(f"{path}: CSV parse error: {exc}")

    return errors, rows


def duplicate_errors(
    rows: list[tuple[str, str, int, Path, int]],
    unique_ids: bool,
    unique_names: bool,
) -> list[str]:
    errors = []

    if unique_ids:
        seen_ids: dict[tuple[str, int], tuple[Path, int]] = {}
        for row_type, _name, row_id, path, line_number in rows:
            key = (row_type, row_id)
            if key in seen_ids:
                first_path, first_line = seen_ids[key]
                errors.append(
                    f"{path}:{line_number}: duplicate {row_type} id {row_id}; "
                    f"first seen at {first_path}:{first_line}"
                )
            else:
                seen_ids[key] = (path, line_number)

    if unique_names:
        seen_names: dict[tuple[str, str], tuple[Path, int]] = {}
        for row_type, name, _row_id, path, line_number in rows:
            key = (row_type, name.casefold())
            if key in seen_names:
                first_path, first_line = seen_names[key]
                errors.append(
                    f"{path}:{line_number}: duplicate {row_type} name {name!r}; "
                    f"first seen at {first_path}:{first_line}"
                )
            else:
                seen_names[key] = (path, line_number)

    return errors


def main() -> int:
    args = parse_args()
    all_errors = []
    all_rows: list[tuple[str, str, int, Path, int]] = []

    for path in args.csv_files:
        errors, rows = validate_file(path)
        all_errors.extend(errors)
        all_rows.extend(rows)

    all_errors.extend(duplicate_errors(all_rows, args.unique_ids, args.unique_names))

    if all_errors:
        print("CSV validation failed:")
        for error in all_errors:
            print(f"- {error}")
        return 1

    type_counts = {"TG": 0, "INDIVIDUAL": 0}
    for row_type, _name, _row_id, _path, _line_number in all_rows:
        type_counts[row_type] += 1

    print("CSV validation passed")
    print(f"files: {len(args.csv_files)}")
    print(f"rows: {len(all_rows)}")
    print(f"TG rows: {type_counts['TG']}")
    print(f"INDIVIDUAL rows: {type_counts['INDIVIDUAL']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

