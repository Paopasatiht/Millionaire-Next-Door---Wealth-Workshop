from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.db_helpers import fetch_all, execute
from utils.date_helpers import current_year

goals_bp = Blueprint('goals', __name__)

HORIZONS = [
    ('lifetime', 'Lifetime Goals', '🏆'),
    ('annual',   'Annual Goals',   '📅'),
    ('monthly',  'Monthly Goals',  '🗓️'),
    ('weekly',   'Weekly Goals',   '📌'),
    ('daily',    'Daily Habits',   '✅'),
]


@goals_bp.route('/goals')
def index():
    year = request.args.get('year', current_year(), type=int)
    all_goals = fetch_all("SELECT * FROM goals ORDER BY created_at", ())
    grouped = {}
    for h, label, icon in HORIZONS:
        items = [g for g in all_goals if g['horizon'] == h]
        done  = sum(1 for g in items if g['status'] == 'done')
        grouped[h] = {'label': label, 'icon': icon, 'goals': items, 'done': done, 'total': len(items)}

    return render_template('goals.html', year=year, grouped=grouped, horizons=HORIZONS)


@goals_bp.route('/goals/add', methods=['POST'])
def add():
    year    = request.form.get('year', current_year(), type=int)
    horizon = request.form.get('horizon', '').strip()
    text    = request.form.get('goal_text', '').strip()
    detail  = request.form.get('target_detail', '').strip()
    deadline = request.form.get('deadline', '').strip()
    if horizon and text:
        execute(
            "INSERT INTO goals (horizon, goal_text, target_detail, deadline, year) VALUES (?,?,?,?,?)",
            (horizon, text, detail, deadline or None, year if horizon == 'annual' else None)
        )
        flash('เพิ่ม Goal สำเร็จ', 'success')
    return redirect(url_for('goals.index', year=year))


@goals_bp.route('/goals/status/<int:goal_id>', methods=['POST'])
def toggle_status(goal_id):
    year   = request.form.get('year', current_year(), type=int)
    status = request.form.get('status', 'active')
    next_status = 'done' if status == 'active' else 'active'
    execute("UPDATE goals SET status=? WHERE id=?", (next_status, goal_id))
    return redirect(url_for('goals.index', year=year))


@goals_bp.route('/goals/delete/<int:goal_id>', methods=['POST'])
def delete(goal_id):
    year = request.form.get('year', current_year(), type=int)
    execute("DELETE FROM goals WHERE id=?", (goal_id,))
    flash('ลบ Goal สำเร็จ', 'success')
    return redirect(url_for('goals.index', year=year))
