# Construction CM Report Automation

An offline-first Python CLI toolkit for Korean construction CM (construction management) cost review workflows.

This project helps construction engineers and CM staff reduce repetitive manual work around construction cost comparison, ready-mixed concrete price review, tower crane cost review, equipment/labor/material price changes, CSV-style data checks, and Markdown report drafting.

The repository is intentionally early-stage. It does not claim existing adoption, fake stars, downloads, or external contributors. It is built as a practical open-source foundation based on real construction management workflow needs, using only synthetic sample data.

## Why this project exists

Construction CM teams often review cost changes across many small line items: base-year price, target-year price, unit, quantity, category, and review notes. The work is important, but the first draft is often repetitive:

- Read CSV or Excel-like data.
- Check whether columns are complete.
- Calculate price differences and percentage changes.
- Summarize category-level impact.
- Draft a report that engineers can review and improve.

This toolkit automates that first pass while keeping the process transparent and reviewable.

## Main features

- CSV loader with required-column validation.
- Numeric cleanup for prices and quantities.
- Price difference and percentage change calculations.
- Optional total impact calculation when quantity is provided.
- Category-level summary for mixed cost data.
- Markdown report generation with executive summary, comparison table, findings, risk notes, and action checklist.
- CLI entry point: `cm-report compare`.
- No paid API calls required.
- Optional future OpenAI API integration can be added without changing the offline core.

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .[dev]
```

For regular use without development tools:

```powershell
python -m pip install -e .
```

## Quick start

Run with the module form:

```powershell
python -m cm_report_automation.cli compare examples/mixed_cost_items.csv --output report.md
```

Run with the package entry point:

```powershell
cm-report compare examples/mixed_cost_items.csv --output report.md
```

The command reads the CSV, calculates changes, generates a Markdown report, and prints a success message.

## Example input

```csv
category,item,base_year,base_price,target_year,target_price,unit,note,quantity
Ready-Mixed Concrete,25 MPa concrete supply,2024,89000,2026,96000,m3,Synthetic review item,1250
Tower Crane,Monthly rental 12-ton class,2024,18000000,2026,20500000,month,Synthetic review item,6
```

## Example output

```text
Report written to report.md
Items reviewed: 2
Categories reviewed: 2
Largest increase: Monthly rental 12-ton class (+13.89%)
```

The generated Markdown report includes:

- Executive summary.
- Cost comparison table.
- Key findings.
- Risk notes.
- Next action checklist.

## Project structure

```text
construction-cm-report-automation/
|-- docs/
|-- examples/
|-- src/cm_report_automation/
|-- tests/
`-- .github/workflows/
```

## Roadmap

- Add Excel import support.
- Add Korean/English bilingual report templates.
- Add optional OpenAI API-assisted report review.
- Add GitHub Issue export for review findings.
- Add more construction-specific templates for material, labor, equipment, and subcontract cost changes.

## Contribution guide summary

Contributions are welcome. Good first contributions include:

- Additional synthetic construction CM sample datasets.
- Better report wording.
- New validation rules.
- Tests for edge cases.
- Documentation improvements.

Please keep all examples synthetic and avoid confidential company, client, or project data.

## License

MIT License. See [LICENSE](LICENSE).

## Honest project status

This is an early-stage open-source toolkit. It is ready for local use, testing, and extension, but it should not be treated as a substitute for professional cost review, contract review, or engineering judgment.
