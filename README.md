# MND Wealth Workshop

A personal finance framework inspired by *The Millionaire Next Door*, designed to be repeated every year with an Excel-based tracking system.

---

## What's Been Built

### Repo Structure

```
mnd-wealth-framework/
├── docs/
│   ├── methodology.md        # PAW/UAW principles + 4 core diagnostic questions
│   └── question-bank.md      # Question sets for monthly / quarterly / annual reviews
├── templates/
│   └── wealth-tracker-template.xlsx   # Blank 6-sheet Excel workbook
├── instances/                # PRIVATE — excluded via .gitignore
│   └── 2026/wealth-tracker-2026.xlsx
└── scripts/
    ├── create_template.py    # Re-generate the blank Excel template
    └── rollover.py           # Carry forward net worth into next year's file
```

### Excel Template — 6 Sheets

| Sheet | Purpose | MND Question |
|---|---|---|
| **Dashboard** | PAW/UAW calculator, savings rate, annual KPIs | Overview |
| **Annual_Budget** | Thai-language expense categories, budget vs. actual | Q2 |
| **Monthly_Log** | 15-min monthly check-in (income, expenses, savings rate, net worth) | Q1–2 |
| **Goals_Matrix** | 5-horizon goal tree: daily → weekly → monthly → annual → lifetime | Q3 |
| **Planning_Time_Log** | Hours spent per month on financial planning (target ≥ 8 hrs) | Q4 |
| **Review_Log** | Annual reflection questions (wealth, budget, goals, planning, commitments) | All |

### Scripts

- **`create_template.py`** — run once to generate a fresh blank `.xlsx` from scratch
- **`rollover.py`** — reads December net worth from the current year's file and writes it as the opening baseline in next year's file; clears all data cells while preserving formulas

---

## Annual Cadence

| Frequency | Action |
|---|---|
| Year 1 (Setup) | Set lifetime → annual goals → configure budget categories |
| Monthly | Fill Monthly Log + Planning Time Log (~15 min) |
| Quarterly | Review Goals Matrix |
| Annually | Run `rollover.py` to generate next year's file |

---

## Quick Start

```bash
# 1. Copy blank template into your private instances folder
cp templates/wealth-tracker-template.xlsx instances/2026/wealth-tracker-2026.xlsx

# 2. Fill in your Profile on the Dashboard sheet

# 3. End of year — generate next year's file
python scripts/rollover.py --source instances/2026/wealth-tracker-2026.xlsx --year 2027
```

---

## Privacy Note

The `instances/` folder contains real financial data and is excluded from version control via `.gitignore`. Only the framework, blank templates, and scripts live in this repo.

---

## Roadmap

- [ ] HTML workshop interface for reviewing and filling in annual goals
- [ ] Expand `question-bank.md` with questions from chapters 3–9
- [ ] Add PAW/UAW trend chart to Dashboard sheet
