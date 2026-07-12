# MND Wealth Workshop

A personal finance framework inspired by *The Millionaire Next Door*, built as a local Flask + SQLite web app. All financial data stays on your machine — only the project code lives on GitHub.

---

## Quick Start

```bash
cd src
python main.py
# Open http://127.0.0.1:5000
```

First run → setup page (name / birth year / annual income) → data auto-saved to `data/mnd-data.db`

---

## What's Been Built

### Stack
- **Backend:** Python Flask, SQLite (via `data/mnd-data.db` — gitignored)
- **Frontend:** Jinja2 templates, vanilla CSS/JS — dark navy theme, Thai UI
- **Scripts:** openpyxl for Excel export, rollover script for year-end

### Project Structure

```
MND/
├── src/
│   ├── main.py               ← entry point: cd src && python main.py
│   ├── app.py                ← Flask factory, register blueprints
│   ├── db.py                 ← SQLite init, 7 tables, seed defaults
│   ├── routes/
│   │   ├── dashboard.py      ← GET /
│   │   ├── monthly.py        ← GET/POST /monthly
│   │   ├── budget.py         ← GET/POST /budget
│   │   ├── goals.py          ← GET/POST /goals
│   │   ├── planning.py       ← GET/POST /planning
│   │   ├── review.py         ← GET/POST /review
│   │   └── export.py         ← GET /export → .xlsx download
│   ├── utils/
│   │   ├── paw.py            ← PAW/UAW calc, savings rate
│   │   ├── db_helpers.py     ← fetch_one, fetch_all, upsert
│   │   ├── date_helpers.py   ← Thai month names, year/month helpers
│   │   └── excel.py          ← openpyxl export workbook
│   ├── templates/            ← Jinja2 HTML (base + 7 pages)
│   └── static/               ← style.css, app.js
├── data/                     ← .gitignore — DB lives here only
├── docs/
│   ├── methodology.md        ← PAW/UAW principles from the book
│   └── question-bank.md      ← 4 core questions + review sets
├── scripts/
│   ├── create_template.py    ← generate blank Excel template
│   └── rollover.py           ← carry net worth to new year
├── templates/
│   └── wealth-tracker-template.xlsx
└── project_planner/          ← concept & planning HTMLs
```

### Database — 7 Tables

| Table | Purpose |
|---|---|
| `profile` | Name, birth year, annual income |
| `budget_categories` | Expense categories per year with monthly budget |
| `monthly_expense_detail` | Actual spend per category per month |
| `monthly_log` | Income, total expenses, savings rate, net worth per month |
| `goals` | Goals across 5 horizons (daily → lifetime) |
| `planning_log` | Planning hours, topics, insights per month |
| `annual_review` | Answers to year-end review questions |

### Pages

| Route | Page | Features |
|---|---|---|
| `/` | Dashboard | PAW/UAW status, multiplier, savings rate, net worth chart, KPIs |
| `/monthly` | Monthly Log | Auto-opens current month, income pre-filled from profile, per-category actual entry, auto-sum expenses + savings rate |
| `/budget` | Annual Budget | Budget vs actual per category, inline add sub-category per group, progress bars, auto-updates from monthly entries |
| `/goals` | Goals Matrix | 5 horizons (daily/weekly/monthly/annual/lifetime), toggle done/active, add/delete |
| `/planning` | Planning Time | Hours per month vs 8hr target, color-coded, topics + insights |
| `/review` | Annual Review | Guided Q&A across 5 sections, progress tracking |
| `/export` | Export Excel | Download full year data as .xlsx |
| `/setup` | First-run Setup | Profile creation, redirected automatically on first visit |

---

## Annual Cadence

| Frequency | Action |
|---|---|
| Year 1 (Setup) | `python main.py` → setup profile → set Budget categories → set Goals |
| Monthly | Open `/monthly` → current month auto-opens → fill actuals per category |
| Quarterly | Review Goals Matrix |
| Year-end | Fill Annual Review → run `python scripts/rollover.py --source ... --year YYYY` |

---

## Privacy

`data/` is in `.gitignore` — your financial data never leaves your machine. GitHub receives only code and blank templates.

---

## Requirements

```bash
pip install flask openpyxl
```
