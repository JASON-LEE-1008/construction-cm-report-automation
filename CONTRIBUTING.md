# Contributing

Thanks for helping improve Construction CM Report Automation.

## Good first contributions

- Add synthetic sample data for construction cost review workflows.
- Improve report wording for CM engineers and project managers.
- Add validation rules for unit consistency.
- Add tests for invalid data and edge cases.
- Extend documentation with safe usage examples.

## Development setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .[dev]
pytest
ruff check .
```

## Data rules

- Do not include confidential company data.
- Do not include real client names or actual internal project names.
- Keep all examples synthetic.
- Do not publish contract-sensitive pricing details from a real project.

## Pull request checklist

- Tests pass.
- New behavior is documented.
- Sample data is synthetic.
- The report output remains clear and reviewable.
