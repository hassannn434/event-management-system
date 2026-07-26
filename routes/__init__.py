"""
Route blueprints package.
Registers all Flask blueprints with the main application.
"""

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.events import events_bp
from routes.registrations import registrations_bp


def register_blueprints(app):
    """Register all application blueprints with the Flask app."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(registrations_bp)
