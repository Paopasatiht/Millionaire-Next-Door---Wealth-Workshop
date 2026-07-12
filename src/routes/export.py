from flask import Blueprint, send_file, request
from utils.excel import export_workbook
from utils.date_helpers import current_year

export_bp = Blueprint('export', __name__)


@export_bp.route('/export')
def export():
    year = request.args.get('year', current_year(), type=int)
    buf  = export_workbook(year)
    return send_file(
        buf,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'mnd-wealth-{year}.xlsx',
    )
