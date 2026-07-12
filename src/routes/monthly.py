from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.db_helpers import fetch_all, upsert
from utils.paw import calc_savings_rate
from utils.date_helpers import current_year, current_month, months_list, years_range

monthly_bp = Blueprint('monthly', __name__)


@monthly_bp.route('/monthly')
def index():
    year = request.args.get('year', current_year(), type=int)
    rows = fetch_all("SELECT * FROM monthly_log WHERE year=? ORDER BY month", (year,))
    row_map = {r['month']: r for r in rows}
    months = months_list()
    for m in months:
        m['data'] = row_map.get(m['num'])

    total_income   = sum(r.get('income', 0)   for r in rows)
    total_expenses = sum(r.get('expenses', 0) for r in rows)
    avg_rate = round(sum(r.get('savings_rate', 0) for r in rows) / len(rows), 1) if rows else 0
    latest_nw = rows[-1]['net_worth'] if rows else 0

    return render_template('monthly.html',
        year=year,
        years=years_range(),
        months=months,
        current_month=current_month(),
        total_income=total_income,
        total_expenses=total_expenses,
        avg_rate=avg_rate,
        latest_nw=latest_nw,
    )


@monthly_bp.route('/monthly/save', methods=['POST'])
def save():
    year  = request.form.get('year', type=int)
    month = request.form.get('month', type=int)
    income   = request.form.get('income', 0, type=float)
    expenses = request.form.get('expenses', 0, type=float)
    net_worth    = request.form.get('net_worth', 0, type=float)
    top_overspend = request.form.get('top_overspend', '').strip()
    note          = request.form.get('note', '').strip()
    savings_rate  = calc_savings_rate(income, expenses)

    upsert('monthly_log', {
        'year': year, 'month': month,
        'income': income, 'expenses': expenses,
        'savings_rate': savings_rate,
        'net_worth': net_worth,
        'top_overspend': top_overspend,
        'note': note,
    }, ['year', 'month'])

    flash(f'บันทึกข้อมูลเดือนสำเร็จ', 'success')
    return redirect(url_for('monthly.index', year=year))
