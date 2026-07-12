from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.db_helpers import fetch_all, fetch_one, upsert, execute
from utils.paw import calc_savings_rate
from utils.date_helpers import current_year, current_month, months_list, years_range
from db import get_connection

monthly_bp = Blueprint('monthly', __name__)


def _budget_grouped(year: int) -> dict:
    rows = fetch_all(
        "SELECT * FROM budget_categories WHERE year=? ORDER BY category, sub_category",
        (year,)
    )
    grouped = {}
    for r in rows:
        grouped.setdefault(r['category'], []).append(r)
    return grouped


def _expense_detail_map(year: int, month: int) -> dict:
    rows = fetch_all(
        "SELECT budget_category_id, actual FROM monthly_expense_detail WHERE year=? AND month=?",
        (year, month)
    )
    return {r['budget_category_id']: r['actual'] for r in rows}


def _refresh_actual_ytd(year: int, cat_id: int):
    total = fetch_one(
        "SELECT COALESCE(SUM(actual),0) as s FROM monthly_expense_detail WHERE year=? AND budget_category_id=?",
        (year, cat_id)
    )
    execute(
        "UPDATE budget_categories SET actual_ytd=? WHERE id=?",
        (total['s'], cat_id)
    )


@monthly_bp.route('/monthly')
def index():
    year    = request.args.get('year', current_year(), type=int)
    profile = fetch_one("SELECT * FROM profile WHERE id=1")
    monthly_income = round((profile['annual_income'] or 0) / 12, 2) if profile else 0

    rows    = fetch_all("SELECT * FROM monthly_log WHERE year=? ORDER BY month", (year,))
    row_map = {r['month']: r for r in rows}
    months  = months_list()
    for m in months:
        m['data']           = row_map.get(m['num'])
        m['expense_detail'] = _expense_detail_map(year, m['num'])

    budget_grouped = _budget_grouped(year)
    has_budget     = bool(budget_grouped)

    total_income   = sum(r.get('income', 0)   for r in rows)
    total_expenses = sum(r.get('expenses', 0) for r in rows)
    avg_rate       = round(sum(r.get('savings_rate', 0) for r in rows) / len(rows), 1) if rows else 0
    latest_nw      = rows[-1]['net_worth'] if rows else 0

    return render_template('monthly.html',
        year=year, years=years_range(),
        months=months,
        current_month=current_month(),
        monthly_income=monthly_income,
        budget_grouped=budget_grouped,
        has_budget=has_budget,
        total_income=total_income,
        total_expenses=total_expenses,
        avg_rate=avg_rate,
        latest_nw=latest_nw,
    )


@monthly_bp.route('/monthly/save', methods=['POST'])
def save():
    year      = request.form.get('year', type=int)
    month     = request.form.get('month', type=int)
    income    = request.form.get('income', 0, type=float)
    net_worth = request.form.get('net_worth', 0, type=float)
    note      = request.form.get('note', '').strip()

    # Collect per-category actuals (budget-linked mode)
    cat_ids     = request.form.getlist('cat_id')
    cat_actuals = {}
    for cid in cat_ids:
        val = request.form.get(f'actual_{cid}', 0, type=float)
        cat_actuals[int(cid)] = val

    # Simple mode fallback (no budget set)
    if cat_ids:
        total_expenses = sum(cat_actuals.values())
    else:
        total_expenses = request.form.get('expenses_simple', 0, type=float)

    # Find top overspend category
    top_overspend = ''
    if cat_ids:
        budgets = fetch_all(
            f"SELECT id, sub_category, monthly_budget FROM budget_categories WHERE id IN ({','.join(cat_ids)})",
            ()
        )
        budget_map = {r['id']: r for r in budgets}
        worst_diff = 0
        for cid, actual in cat_actuals.items():
            budget = (budget_map.get(cid) or {}).get('monthly_budget') or 0
            diff   = actual - budget
            if diff > worst_diff:
                worst_diff    = diff
                top_overspend = (budget_map.get(cid) or {}).get('sub_category', '')

    savings_rate = calc_savings_rate(income, total_expenses)

    # Save monthly log
    upsert('monthly_log', {
        'year': year, 'month': month,
        'income': income, 'expenses': total_expenses,
        'savings_rate': savings_rate,
        'net_worth': net_worth,
        'top_overspend': top_overspend,
        'note': note,
    }, ['year', 'month'])

    # Save expense details + refresh actual_ytd
    con = get_connection()
    for cid, actual in cat_actuals.items():
        con.execute(
            "INSERT INTO monthly_expense_detail (year, month, budget_category_id, actual) "
            "VALUES (?,?,?,?) ON CONFLICT(year,month,budget_category_id) DO UPDATE SET actual=excluded.actual",
            (year, month, cid, actual)
        )
    con.commit()
    con.close()

    for cid in cat_actuals:
        _refresh_actual_ytd(year, cid)

    flash('บันทึกข้อมูลเดือนสำเร็จ', 'success')
    return redirect(url_for('monthly.index', year=year))
