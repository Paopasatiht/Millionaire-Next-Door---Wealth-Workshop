from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.db_helpers import fetch_all, fetch_one, execute
from utils.date_helpers import current_year, years_range
from db import DEFAULT_CATEGORIES, get_connection

budget_bp = Blueprint('budget', __name__)


def _ensure_categories(year: int):
    count = fetch_one("SELECT COUNT(*) as c FROM budget_categories WHERE year=?", (year,))
    if count and count['c'] == 0:
        con = get_connection()
        con.executemany(
            "INSERT INTO budget_categories (year, category, sub_category) VALUES (?,?,?)",
            [(year, cat, sub) for cat, sub in DEFAULT_CATEGORIES]
        )
        con.commit()
        con.close()


@budget_bp.route('/budget')
def index():
    year = request.args.get('year', current_year(), type=int)
    _ensure_categories(year)
    rows = fetch_all(
        "SELECT * FROM budget_categories WHERE year=? ORDER BY category, sub_category", (year,)
    )

    # Group by category
    grouped = {}
    total_budget = 0
    total_actual = 0
    for r in rows:
        cat = r['category']
        annual = (r['monthly_budget'] or 0) * 12
        actual = r['actual_ytd'] or 0
        r['annual_budget'] = annual
        r['variance'] = annual - actual
        r['pct'] = round(actual / annual * 100) if annual else 0
        total_budget += annual
        total_actual += actual
        grouped.setdefault(cat, []).append(r)

    return render_template('budget.html',
        year=year, years=years_range(),
        grouped=grouped,
        total_budget=total_budget,
        total_actual=total_actual,
        total_variance=total_budget - total_actual,
        total_pct=round(total_actual / total_budget * 100) if total_budget else 0,
    )


@budget_bp.route('/budget/save', methods=['POST'])
def save():
    year = request.form.get('year', type=int)
    ids   = request.form.getlist('id')
    for row_id in ids:
        monthly_budget = request.form.get(f'monthly_budget_{row_id}', 0, type=float)
        actual_ytd     = request.form.get(f'actual_ytd_{row_id}', 0, type=float)
        execute(
            "UPDATE budget_categories SET monthly_budget=?, actual_ytd=? WHERE id=?",
            (monthly_budget, actual_ytd, int(row_id))
        )
    flash('บันทึก Budget สำเร็จ', 'success')
    return redirect(url_for('budget.index', year=year))


@budget_bp.route('/budget/add', methods=['POST'])
def add_category():
    year     = request.form.get('year', type=int)
    category = request.form.get('category', '').strip()
    sub      = request.form.get('sub_category', '').strip()
    if category and sub:
        execute(
            "INSERT INTO budget_categories (year, category, sub_category) VALUES (?,?,?)",
            (year, category, sub)
        )
        flash('เพิ่มหมวดสำเร็จ', 'success')
    return redirect(url_for('budget.index', year=year))


@budget_bp.route('/budget/delete/<int:row_id>', methods=['POST'])
def delete_category(row_id):
    year = request.form.get('year', type=int)
    execute("DELETE FROM budget_categories WHERE id=?", (row_id,))
    flash('ลบหมวดสำเร็จ', 'success')
    return redirect(url_for('budget.index', year=year))
