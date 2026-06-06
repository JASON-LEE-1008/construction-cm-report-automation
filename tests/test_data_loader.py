from __future__ import annotations

import pytest

from cm_report_automation.data_loader import CSVValidationError, load_cost_items


def test_load_cost_items_from_example() -> None:
    items = load_cost_items("examples/mixed_cost_items.csv")

    assert len(items) == 6
    assert items[0].category == "Ready-Mixed Concrete"
    assert items[0].base_price == 89000
    assert items[0].quantity == 1250


def test_missing_required_column_raises(tmp_path) -> None:
    csv_path = tmp_path / "invalid.csv"
    csv_path.write_text(
        "category,item,base_year,base_price,target_year,target_price,unit\n"
        "Material,Rebar,2024,940000,2026,1010000,ton\n",
        encoding="utf-8",
    )

    with pytest.raises(CSVValidationError, match="note"):
        load_cost_items(csv_path)


def test_invalid_numeric_value_raises(tmp_path) -> None:
    csv_path = tmp_path / "invalid-number.csv"
    csv_path.write_text(
        "category,item,base_year,base_price,target_year,target_price,unit,note\n"
        "Material,Rebar,2024,not-a-number,2026,1010000,ton,Synthetic\n",
        encoding="utf-8",
    )

    with pytest.raises(CSVValidationError, match="base_price"):
        load_cost_items(csv_path)
