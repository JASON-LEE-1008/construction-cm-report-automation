from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

REQUIRED_COLUMNS = {
    "category",
    "item",
    "base_year",
    "base_price",
    "target_year",
    "target_price",
    "unit",
    "note",
}


class CSVValidationError(ValueError):
    """Raised when an input CSV cannot be validated."""


@dataclass(frozen=True)
class CostItem:
    category: str
    item: str
    base_year: int
    base_price: float
    target_year: int
    target_price: float
    unit: str
    note: str
    quantity: float | None = None


def load_cost_items(path: str | Path) -> list[CostItem]:
    """Load and validate construction cost items from a CSV file."""
    source = Path(path)
    if not source.exists():
        raise CSVValidationError(f"CSV file not found: {source}")

    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise CSVValidationError("CSV file is empty or missing a header row.")

        normalized_headers = {header.strip() for header in reader.fieldnames}
        missing = REQUIRED_COLUMNS - normalized_headers
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise CSVValidationError(f"CSV is missing required columns: {missing_list}")

        items: list[CostItem] = []
        for row_number, row in enumerate(reader, start=2):
            items.append(_row_to_cost_item(row, row_number))

    if not items:
        raise CSVValidationError("CSV contains a header row but no cost items.")
    return items


def _row_to_cost_item(row: dict[str, str | None], row_number: int) -> CostItem:
    cleaned = {
        str(key).strip(): "" if value is None else value.strip() for key, value in row.items()
    }
    category = _required_text(cleaned, "category", row_number)
    item = _required_text(cleaned, "item", row_number)
    unit = _required_text(cleaned, "unit", row_number)

    return CostItem(
        category=category,
        item=item,
        base_year=int(_parse_number(cleaned.get("base_year"), "base_year", row_number)),
        base_price=_parse_number(cleaned.get("base_price"), "base_price", row_number),
        target_year=int(_parse_number(cleaned.get("target_year"), "target_year", row_number)),
        target_price=_parse_number(cleaned.get("target_price"), "target_price", row_number),
        unit=unit,
        note=cleaned.get("note", ""),
        quantity=_parse_optional_number(cleaned.get("quantity"), "quantity", row_number),
    )


def _required_text(row: dict[str, str], field: str, row_number: int) -> str:
    value = row.get(field, "").strip()
    if not value:
        raise CSVValidationError(f"Row {row_number}: '{field}' is required.")
    return value


def _parse_optional_number(value: str | None, field: str, row_number: int) -> float | None:
    if value is None or value.strip() == "":
        return None
    return _parse_number(value, field, row_number)


def _parse_number(value: str | None, field: str, row_number: int) -> float:
    if value is None or value.strip() == "":
        raise CSVValidationError(f"Row {row_number}: '{field}' is required.")

    normalized = re.sub(r"[,\s]", "", value)
    try:
        return float(normalized)
    except ValueError as exc:
        raise CSVValidationError(
            f"Row {row_number}: '{field}' must be a valid number, got {value!r}."
        ) from exc
