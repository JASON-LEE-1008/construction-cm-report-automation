from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .cost_compare import compare_costs, largest_increase, summarize_by_category
from .data_loader import CSVValidationError, load_cost_items
from .report_generator import write_markdown_report
from .templates import DEFAULT_REPORT_TITLE


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cm-report",
        description="Generate construction CM cost comparison Markdown reports from CSV files.",
    )
    subparsers = parser.add_subparsers(dest="command")

    compare_parser = subparsers.add_parser("compare", help="Compare cost items from a CSV file.")
    compare_parser.add_argument("csv_path", help="Input CSV file path.")
    compare_parser.add_argument(
        "--output",
        "-o",
        default="report.md",
        help="Output Markdown report path.",
    )
    compare_parser.add_argument(
        "--title",
        default=DEFAULT_REPORT_TITLE,
        help="Report title.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "compare":
        parser.print_help()
        return 1

    try:
        items = load_cost_items(Path(args.csv_path))
        results = compare_costs(items)
        write_markdown_report(results, args.output, title=args.title)
    except CSVValidationError as exc:
        print(f"Could not process CSV: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Could not write report: {exc}", file=sys.stderr)
        return 3

    summaries = summarize_by_category(results)
    increase = largest_increase(results)
    print(f"Report written to {args.output}")
    print(f"Items reviewed: {len(results)}")
    print(f"Categories reviewed: {len(summaries)}")
    if increase:
        print(f"Largest increase: {increase.item} ({increase.percentage_change:+.2f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
