from __future__ import annotations

from datetime import date
from pathlib import Path

from .cost_compare import (
    CategorySummary,
    ComparisonResult,
    largest_decrease,
    largest_increase,
    summarize_by_category,
)
from .templates import DEFAULT_REPORT_TITLE, NEXT_ACTIONS, RISK_NOTES


def generate_markdown_report(
    results: list[ComparisonResult],
    title: str = DEFAULT_REPORT_TITLE,
    generated_on: date | None = None,
) -> str:
    generated_on = generated_on or date.today()
    summaries = summarize_by_category(results)

    lines: list[str] = [
        f"# {title}",
        "",
        f"Generated date: {generated_on.isoformat()}",
        "",
        "## Executive Summary",
        "",
        *_executive_summary(results, summaries),
        "",
        "## Category Summary",
        "",
        "| Category | Items | Average Change | Total Impact | Up | Down | Flat |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for summary in summaries:
        summary_row = (
            f"| {_cell(summary.category)} | {summary.item_count} | "
            f"{_format_percent(summary.average_percentage_change)} | "
            f"{_format_currency(summary.total_impact)} | "
            f"{summary.increased_items} | {summary.decreased_items} | "
            f"{summary.unchanged_items} |"
        )
        lines.append(summary_row)

    lines.extend(
        [
            "",
            "## Cost Comparison Table",
            "",
            "| Category | Item | Base | Target | Difference | Change | Quantity | Impact | Note |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )

    for result in results:
        base = f"{_format_currency(result.base_price)} / {result.unit}"
        target = f"{_format_currency(result.target_price)} / {result.unit}"
        comparison_row = (
            f"| {_cell(result.category)} | {_cell(result.item)} | "
            f"{base} | {target} | {_format_currency(result.price_difference)} | "
            f"{_format_percent(result.percentage_change)} | {_format_number(result.quantity)} | "
            f"{_format_currency(result.total_impact)} | {_cell(result.note)} |"
        )
        lines.append(comparison_row)

    lines.extend(["", "## Key Findings", "", *_key_findings(results), ""])
    lines.extend(["## Risk Notes", ""])
    lines.extend(f"- {note}" for note in RISK_NOTES)
    lines.extend(["", "## Next Action Checklist", ""])
    lines.extend(f"- [ ] {action}" for action in NEXT_ACTIONS)
    lines.append("")

    return "\n".join(lines)


def write_markdown_report(
    results: list[ComparisonResult],
    output_path: str | Path,
    title: str = DEFAULT_REPORT_TITLE,
) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        generate_markdown_report(results, title=title),
        encoding="utf-8",
    )


def _executive_summary(
    results: list[ComparisonResult],
    summaries: list[CategorySummary],
) -> list[str]:
    total_impact_values = [
        result.total_impact for result in results if result.total_impact is not None
    ]
    total_impact = sum(total_impact_values) if total_impact_values else None
    increase = largest_increase(results)
    decrease = largest_decrease(results)

    lines = [
        f"- Items reviewed: {len(results)}",
        f"- Categories reviewed: {len(summaries)}",
        f"- Estimated total impact from rows with quantity: {_format_currency(total_impact)}",
    ]
    if increase:
        change = _format_percent(increase.percentage_change)
        lines.append(f"- Largest percentage increase: {increase.item} ({change})")
    if decrease:
        change = _format_percent(decrease.percentage_change)
        lines.append(f"- Largest percentage decrease: {decrease.item} ({change})")
    return lines


def _key_findings(results: list[ComparisonResult]) -> list[str]:
    if not results:
        return ["- No cost items were reviewed."]

    ranked = sorted(
        results,
        key=lambda result: abs(result.percentage_change or 0),
        reverse=True,
    )
    findings = []
    for result in ranked[:5]:
        difference = _format_currency(result.price_difference)
        change = _format_percent(result.percentage_change)
        finding = f"- {result.item}: {result.trend} of {difference} per {result.unit} ({change})."
        findings.append(finding)
    return findings


def _format_currency(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:,.0f}"


def _format_number(value: float | None) -> str:
    if value is None:
        return "N/A"
    if value.is_integer():
        return f"{value:,.0f}"
    return f"{value:,.2f}"


def _format_percent(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:+.2f}%"


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")
