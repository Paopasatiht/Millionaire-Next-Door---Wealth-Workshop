# MND Wealth Workshop

A personal finance framework inspired by *The Millionaire Next Door*, designed to be repeated every year with an Excel-based tracking system.

## Structure

```
mnd-wealth-framework/
├── docs/
│   ├── methodology.md        # Core principles from the book
│   └── question-bank.md      # The 4 diagnostic questions + expansions
├── templates/
│   └── wealth-tracker-template.xlsx   # Blank template (no year-specific data)
├── instances/                # PRIVATE — add to .gitignore or use private repo
│   └── 2026/wealth-tracker-2026.xlsx
└── scripts/
    └── rollover.py           # Generate next year's file from current year
```

## Annual Cadence

| Frequency | Action |
|---|---|
| Year 1 (Setup) | Set lifetime → annual → budget categories |
| Monthly | Fill Monthly Log + Planning Time Log (~15 min) |
| Quarterly | Review Goals Matrix |
| Annually | Run `rollover.py` to carry forward net worth as new baseline |

## Quick Start

```bash
# Generate next year's tracker
python scripts/rollover.py --source instances/2026/wealth-tracker-2026.xlsx --year 2027
```

## Privacy Note

The `instances/` folder contains real financial data and is excluded from version control via `.gitignore`. Keep only the framework and blank templates in this public repo.
