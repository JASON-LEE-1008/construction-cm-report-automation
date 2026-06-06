# Usage

## Required CSV columns

The input CSV must include these columns:

| Column | Description |
| --- | --- |
| `category` | Cost category such as Tower Crane, Ready-Mixed Concrete, Labor, Material, or Equipment. |
| `item` | Cost item name. |
| `base_year` | Year for the baseline price. |
| `base_price` | Baseline unit price. |
| `target_year` | Year for the target price. |
| `target_price` | Target unit price. |
| `unit` | Unit of measurement, such as m3, ton, month, day, or person-day. |
| `note` | Review note. Can be blank, but the column must exist. |

Optional column:

| Column | Description |
| --- | --- |
| `quantity` | Quantity used to estimate total cost impact. |

## Run a comparison

```powershell
cm-report compare examples/mixed_cost_items.csv --output report.md
```

You can customize the report title:

```powershell
cm-report compare examples/tower_crane_costs.csv --output tower-crane-report.md --title "Tower Crane Cost Review"
```

## Error handling

If a CSV file is missing required columns, the CLI prints a clear error message and exits with a non-zero status.

If a numeric field cannot be parsed, the CLI reports the row number and field name so the file can be fixed quickly.

## Offline-first design

The basic project does not require an API key or paid service. Future OpenAI API integration should remain optional and should not block offline cost review.
