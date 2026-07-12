from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.db_helpers import fetch_all, upsert
from utils.date_helpers import current_year, current_month, months_list, years_range

planning_bp = Blueprint('planning', __name__)

TARGET_HOURS = 8


@planning_bp.route('/planning')
def index():
    year = request.args.get('year', current_year(), type=int)
    rows = fetch_all("SELECT * FROM planning_log WHERE year=? ORDER BY month", (year,))
    row_map = {r['month']: r for r in rows}
    months = months_list()
    for m in months:
        m['data'] = row_map.get(m['num'])

    total_hours  = sum(r.get('hours', 0) for r in rows)
    avg_hours    = round(total_hours / 12, 1)
    months_hit   = sum(1 for r in rows if r.get('hours', 0) >= TARGET_HOURS)

    return render_template('planning.html',
        year=year, years=years_range(),
        months=months,
        current_month=current_month(),
        total_hours=total_hours,
        avg_hours=avg_hours,
        months_hit=months_hit,
        target=TARGET_HOURS,
    )


@planning_bp.route('/planning/save', methods=['POST'])
def save():
    year  = request.form.get('year', type=int)
    month = request.form.get('month', type=int)
    upsert('planning_log', {
        'year':        year,
        'month':       month,
        'hours':       request.form.get('hours', 0, type=float),
        'activities':  request.form.get('activities', '').strip(),
        'topics':      request.form.get('topics', '').strip(),
        'key_insight': request.form.get('key_insight', '').strip(),
        'source':      request.form.get('source', '').strip(),
    }, ['year', 'month'])
    flash('บันทึกสำเร็จ', 'success')
    return redirect(url_for('planning.index', year=year))
