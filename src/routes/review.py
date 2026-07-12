from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.db_helpers import fetch_all, upsert
from utils.date_helpers import current_year, years_range

review_bp = Blueprint('review', __name__)

SECTIONS = [
    ('wealth', 'Wealth Status', [
        ('paw_status',       'PAW / UAW Status ปีนี้?'),
        ('net_worth_change', 'Net Worth เปลี่ยนแปลงเทียบปีที่แล้ว?'),
        ('savings_rate',     'Savings Rate เฉลี่ยทั้งปี?'),
        ('biggest_win',      'ชัยชนะทางการเงินที่ใหญ่ที่สุดปีนี้?'),
        ('biggest_mistake',  'ความผิดพลาดทางการเงินที่ใหญ่ที่สุดปีนี้?'),
    ]),
    ('budget', 'Budget Review', [
        ('budget_followed',      'คุณทำตาม Written Budget ไหม? อธิบาย'),
        ('overspent_categories', '3 หมวดที่บานปลายมากที่สุด?'),
        ('cut_categories',       '3 หมวดที่ลดได้สำเร็จ?'),
    ]),
    ('goals', 'Goals Review', [
        ('annual_goals_done', 'Annual Goals ที่ทำสำเร็จ?'),
        ('goals_carried',     'Goals ที่ carry ไปปีหน้า?'),
        ('lifetime_insight',  'Insight ใหม่เกี่ยวกับ Lifetime Goal?'),
    ]),
    ('planning', 'Planning Review', [
        ('total_hours',  'ชั่วโมงวางแผนรวมทั้งปี?'),
        ('best_source',  'แหล่งความรู้การเงินที่ดีที่สุดปีนี้?'),
        ('top_lessons',  '3 บทเรียนสำคัญที่ได้ปีนี้?'),
    ]),
    ('commitments', 'Next Year Commitments', [
        ('savings_target', 'เป้าหมายออมเงินปีหน้า (฿)?'),
        ('nw_target',      'เป้าหมาย Net Worth ปีหน้า (฿)?'),
        ('habit_start',    'นิสัยที่จะเริ่มทำปีหน้า?'),
        ('habit_stop',     'นิสัยที่จะหยุดทำปีหน้า?'),
    ]),
]


@review_bp.route('/review')
def index():
    year = request.args.get('year', current_year(), type=int)
    rows = fetch_all("SELECT question_key, answer FROM annual_review WHERE year=?", (year,))
    answers = {r['question_key']: r['answer'] for r in rows}
    total_q = sum(len(qs) for _, _, qs in SECTIONS)
    answered = sum(1 for v in answers.values() if v and v.strip())
    return render_template('review.html',
        year=year, years=years_range(),
        sections=SECTIONS,
        answers=answers,
        total_q=total_q,
        answered=answered,
    )


@review_bp.route('/review/save', methods=['POST'])
def save():
    year = request.form.get('year', type=int)
    for _, _, questions in SECTIONS:
        for key, _ in questions:
            answer = request.form.get(key, '').strip()
            upsert('annual_review', {'year': year, 'question_key': key, 'answer': answer,
                                     'updated_at': 'CURRENT_TIMESTAMP'}, ['year', 'question_key'])
    flash('บันทึก Annual Review สำเร็จ', 'success')
    return redirect(url_for('review.index', year=year))
