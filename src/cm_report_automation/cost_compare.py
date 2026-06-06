from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .data_loader import CostItem


@dataclass(frozen=True)
class ComparisonResult:
    category: str
    item: str
    base_year: int
    base_price: float
    target_year: int
    target_price: float
    unit: str
    note: str
    quantity: float | None
    price_difference: float
    percentage_change: float | None
    total_impact: float | None

    @property
    def trend(self) -> str:
        if self.price_difference > 0:
            return "increase"
        if self.price_difference < 0:
            return "decrease"
        return "no change"


@dataclass(frozen=True)
class CategorySummary:
    category: str
    item_count: int
    average_percentage_change: float | None
    total_impact: float | None
    increased_items: int
    decreased_items: int
    unchanged_items: int


def compare_item(item: CostItem) -> ComparisonResult:
    price_difference = item.target_price - item.base_price
    percentage_change = None
    if item.base_price != 0:
        percentage_change = (price_difference / item.base_price) * 100

    total_impact = None
    if item.quantity is not None:
        total_impact = price_difference * item.quantity

    return ComparisonResult(
        category=item.category,
        item=item.item,
        base_year=item.base_year,
        base_price=item.base_price,
        target_year=item.target_year,
        target_price=item.target_price,
        unit=item.unit,
        note=item.note,
        quantity=item.quantity,
        price_difference=price_difference,
        percentage_change=percentage_change,
        total_impact=total_impact,
    )


def compare_costs(items: list[CostItem]) -> list[ComparisonResult]:
    return [compare_item(item) for item in items]


def summarize_by_category(results: list[ComparisonResult]) -> list[CategorySummary]:
    grouped: dict[str, list[ComparisonResult]] = defaultdict(list)
    for result in results:
        grouped[result.category].append(result)

    summaries: list[CategorySummary] = []
    for category, category_results in sorted(grouped.items()):
        percentages = [
            result.percentage_change
            for result in category_results
            if result.percentage_change is not None
        ]
        impacts = [
            result.total_impact for result in category_results if result.total_impact is not None
        ]
        increased_items = sum(1 for result in category_results if result.price_difference > 0)
        decreased_items = sum(1 for result in category_results if result.price_difference < 0)
        unchanged_items = sum(1 for result in category_results if result.price_difference == 0)
        summaries.append(
            CategorySummary(
                category=category,
                item_count=len(category_results),
                average_percentage_change=(
                    sum(percentages) / len(percentages) if percentages else None
                ),
                total_impact=sum(impacts) if impacts else None,
                increased_items=increased_items,
                decreased_items=decreased_items,
                unchanged_items=unchanged_items,
            )
        )
    return summaries


def largest_increase(results: list[ComparisonResult]) -> ComparisonResult | None:
    candidates = [result for result in results if result.percentage_change is not None]
    if not candidates:
        return None
    return max(candidates, key=lambda result: result.percentage_change or 0)


def largest_decrease(results: list[ComparisonResult]) -> ComparisonResult | None:
    candidates = [result for result in results if result.percentage_change is not None]
    if not candidates:
        return None
    return min(candidates, key=lambda result: result.percentage_change or 0)
