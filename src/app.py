from flask import Flask
from db import init_db
from routes.dashboard import dashboard_bp
from routes.monthly import monthly_bp
from routes.budget import budget_bp
from routes.goals import goals_bp
from routes.planning import planning_bp
from routes.review import review_bp
from routes.export import export_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = 'mnd-local-secret-2026'

    init_db()

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(monthly_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(planning_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(export_bp)

    @app.template_filter('fmt_num')
    def fmt_num(value):
        try:
            return f"{float(value):,.0f}"
        except (TypeError, ValueError):
            return value or '-'

    @app.template_filter('fmt_pct')
    def fmt_pct(value):
        try:
            return f"{float(value):.1f}%"
        except (TypeError, ValueError):
            return '-'

    return app
