from __future__ import annotations

from cm_report_automation.cost_compare import compare_costs, compare_item, summarize_by_category
from cm_report_automation.data_loader import CostItem


def test_percentage_change_and_total_impact() -> None:
    item = CostItem(
        category="Material",
        item="Synthetic rebar",
        base_year=2024,
        base_price=100,
        target_year=2026,
        target_price=125,
        unit="ton",
        note="Synthetic test item",
        quantity=10,
    )

    result = compare_item(item)

    assert result.price_difference == 25
    assert result.percentage_change == 25
    assert result.total_impact == 250
    assert result.trend == "increase"


def test_category_summary() -> None:
    items = [
        CostItem("Material", "A", 2024, 100, 2026, 120, "ton", "Synthetic", 10),
        CostItem("Material", "B", 2024, 200, 2026, 180, "ton", "Synthetic", 5),
        CostItem("Labor", "C", 2024, 100, 2026, 100, "day", "Synthetic", 3),
    ]

    summaries = summarize_by_category(compare_costs(items))

    material = next(summary for summary in summaries if summary.category == "Material")
    assert material.item_count == 2
    assert material.increased_items == 1
    assert material.decreased_items == 1
    assert material.total_impact == 100
