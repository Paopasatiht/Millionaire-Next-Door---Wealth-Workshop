from flask import Blueprint, render_template, redirect, url_for
from utils.db_helpers import fetch_one, fetch_all
from utils.paw import calc_expected_nw, get_paw_status, calc_savings_rate
from utils.date_helpers import current_year, MONTHS_SHORT
import datetime

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    profile = fetch_one("SELECT * FROM profile WHERE id=1")
    if not profile:
        return redirect(url_for('dashboard.setup'))

    year = current_year()
    age = year - (profile.get('birth_year') or year)
    income = profile.get('annual_income') or 0

    # Latest net worth from monthly log
    latest = fetch_one(
        "SELECT * FROM monthly_log WHERE year=? ORDER BY month DESC LIMIT 1", (year,)
    )
    net_worth = latest['net_worth'] if latest else 0

    expected = calc_expected_nw(age, income)
    paw = get_paw_status(net_worth, expected)

    # Savings rate average this year
    logs = fetch_all("SELECT * FROM monthly_log WHERE year=? AND income>0", (year,))
    avg_savings = round(sum(r['savings_rate'] for r in logs) / len(logs), 1) if logs else 0

    # Planning hours average
    planning = fetch_all("SELECT hours FROM planning_log WHERE year=?", (year,))
    avg_planning = round(sum(r['hours'] for r in planning) / len(planning), 1) if planning else 0

    # Goals done
    goals_all = fetch_all("SELECT * FROM goals WHERE year=? OR horizon IN ('lifetime','daily','weekly')", (year,))
    goals_done = [g for g in goals_all if g['status'] == 'done']

    # Monthly net worth for chart (all 12 months)
    all_logs = fetch_all("SELECT month, net_worth FROM monthly_log WHERE year=? ORDER BY month", (year,))
    nw_map = {r['month']: r['net_worth'] for r in all_logs}
    chart_data = [{"month": MONTHS_SHORT[m-1], "nw": nw_map.get(m, 0)} for m in range(1, 13)]
    chart_max = max((d['nw'] for d in chart_data), default=1) or 1

    # Budget months followed
    budget_ok = len([l for l in logs if l['savings_rate'] >= 0])

    return render_template('dashboard.html',
        profile=profile,
        year=year,
        age=age,
        net_worth=net_worth,
        expected=expected,
        paw=paw,
        avg_savings=avg_savings,
        avg_planning=avg_planning,
        goals_total=len(goals_all),
        goals_done=len(goals_done),
        chart_data=chart_data,
        chart_max=chart_max,
        budget_ok=budget_ok,
        months_logged=len(logs),
    )


@dashboard_bp.route('/setup', methods=['GET', 'POST'])
def setup():
    from flask import request, flash
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        birth_year = request.form.get('birth_year', type=int)
        annual_income = request.form.get('annual_income', type=float)
        if not name or not birth_year or not annual_income:
            flash('กรุณากรอกข้อมูลให้ครบ', 'error')
            return redirect(url_for('dashboard.setup'))
        from utils.db_helpers import execute
        execute(
            "INSERT INTO profile (id, name, birth_year, annual_income, updated_at) "
            "VALUES (1, ?, ?, ?, CURRENT_TIMESTAMP) "
            "ON CONFLICT(id) DO UPDATE SET name=excluded.name, "
            "birth_year=excluded.birth_year, annual_income=excluded.annual_income, "
            "updated_at=CURRENT_TIMESTAMP",
            (name, birth_year, annual_income)
        )
        flash('บันทึกข้อมูลสำเร็จ', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('setup.html')
