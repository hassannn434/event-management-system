"""
Event Management System - Main Application
Entry point for the Flask web application.
"""

import os
from datetime import datetime
from flask import Flask, render_template, send_from_directory
from config import Config


def _format_date(value, fmt="%b %d, %Y"):
    """Safely format a date value (string or datetime)."""
    if not value:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except (ValueError, TypeError):
            return value
    return value.strftime(fmt)


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["UPLOAD_FOLDER"] = Config.UPLOAD_FOLDER

    app.jinja_env.filters["format_date"] = _format_date

    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    from models.db import init_sqlite_db
    init_sqlite_db()

    from routes import register_blueprints
    register_blueprints(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("500.html"), 500

    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {"now": datetime.now()}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
