from __future__ import annotations

from datetime import date

from cm_report_automation.cost_compare import compare_costs
from cm_report_automation.data_loader import CostItem
from cm_report_automation.report_generator import generate_markdown_report


def test_markdown_report_creation() -> None:
    items = [
        CostItem(
            category="Ready-Mixed Concrete",
            item="25 MPa concrete supply",
            base_year=2024,
            base_price=89000,
            target_year=2026,
            target_price=96000,
            unit="m3",
            note="Synthetic review item",
            quantity=1250,
        )
    ]
    report = generate_markdown_report(
        compare_costs(items),
        title="Synthetic CM Report",
        generated_on=date(2026, 6, 7),
    )

    assert "# Synthetic CM Report" in report
    assert "Executive Summary" in report
    assert "25 MPa concrete supply" in report
    assert "Next Action Checklist" in report
    assert "+7.87%" in report
