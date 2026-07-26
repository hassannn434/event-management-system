"""
User routes.
Handles user dashboard and profile management.
"""

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.db import fetch_one, fetch_all, execute_query

user_bp = Blueprint("user", __name__, url_prefix="/user")


def user_required(f):
    """Decorator to restrict access to logged-in users."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "user":
            flash("Access denied. Please login.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


@user_bp.route("/dashboard")
@user_required
def dashboard():
    """Display user dashboard with registered events and stats."""
    user_id = session["user_id"]
    stats = {
        "registered_events": fetch_one(
            """SELECT COUNT(*) as count FROM registrations
               WHERE user_id = %s AND status = 'Registered'""",
            (user_id,),
        )["count"],
        "upcoming_events": fetch_one(
            """SELECT COUNT(*) as count FROM registrations r
               JOIN events e ON r.event_id = e.id
               WHERE r.user_id = %s AND r.status = 'Registered' AND e.event_date >= CURDATE()""",
            (user_id,),
        )["count"],
        "completed_events": fetch_one(
            """SELECT COUNT(*) as count FROM registrations r
               JOIN events e ON r.event_id = e.id
               WHERE r.user_id = %s AND r.status = 'Registered' AND e.status = 'Completed'""",
            (user_id,),
        )["count"],
    }
    upcoming = fetch_all(
        """SELECT e.*, c.name as category_name FROM registrations r
           JOIN events e ON r.event_id = e.id
           LEFT JOIN categories c ON e.category_id = c.id
           WHERE r.user_id = %s AND r.status = 'Registered' AND e.event_date >= CURDATE()
           ORDER BY e.event_date LIMIT 5""",
        (user_id,),
    )
    return render_template("dashboard_user.html", stats=stats, upcoming=upcoming)


@user_bp.route("/profile", methods=["GET", "POST"])
@user_required
def profile():
    """View and edit user profile."""
    user = fetch_one("SELECT * FROM users WHERE id = %s", (session["user_id"],))
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("user.dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        city = request.form.get("city", "").strip()
        bio = request.form.get("bio", "").strip()

        if not name:
            flash("Name is required.", "danger")
            return render_template("profile.html", user=user)

        execute_query(
            "UPDATE users SET name=%s, phone=%s, city=%s, bio=%s WHERE id=%s",
            (name, phone, city, bio, session["user_id"]),
        )
        session["user_name"] = name
        flash("Profile updated successfully!", "success")
        return redirect(url_for("user.profile"))

    return render_template("profile.html", user=user)


@user_bp.route("/change-password", methods=["POST"])
@user_required
def change_password():
    """Change user password."""
    current_password = request.form.get("current_password", "").strip()
    new_password = request.form.get("new_password", "").strip()
    confirm_password = request.form.get("confirm_password", "").strip()

    user = fetch_one(
        "SELECT * FROM users WHERE id = %s AND password = %s",
        (session["user_id"], current_password),
    )
    if not user:
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("user.profile"))

    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("user.profile"))

    if len(new_password) < 6:
        flash("Password must be at least 6 characters.", "danger")
        return redirect(url_for("user.profile"))

    execute_query(
        "UPDATE users SET password = %s WHERE id = %s",
        (new_password, session["user_id"]),
    )
    flash("Password changed successfully!", "success")
    return redirect(url_for("user.profile"))
