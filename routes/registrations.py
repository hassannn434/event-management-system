"""
Registration routes.
Handles event registration, cancellation, and viewing registered events.
"""

from datetime import date
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.db import fetch_one, fetch_all, execute_query, execute_insert

registrations_bp = Blueprint("registrations", __name__, url_prefix="/registrations")


def user_required(f):
    """Decorator to restrict access to logged-in users."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "user":
            flash("Access denied. Please login.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


@registrations_bp.route("/register/<int:event_id>", methods=["POST"])
@user_required
def register_for_event(event_id):
    """Register the current user for an event."""
    user_id = session["user_id"]
    event = fetch_one("SELECT * FROM events WHERE id = %s", (event_id,))
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for("events.list_events"))

    if event["status"] != "Upcoming":
        flash("Registration is closed for this event.", "danger")
        return redirect(url_for("events.event_detail", event_id=event_id))

    today = date.today().isoformat()
    if event["registration_deadline"] < today:
        flash("Registration deadline has passed.", "danger")
        return redirect(url_for("events.event_detail", event_id=event_id))

    existing = fetch_one(
        """SELECT id FROM registrations
           WHERE user_id = %s AND event_id = %s AND status = 'Registered'""",
        (user_id, event_id),
    )
    if existing:
        flash("You are already registered for this event.", "warning")
        return redirect(url_for("events.event_detail", event_id=event_id))

    count = fetch_one(
        """SELECT COUNT(*) as count FROM registrations
           WHERE event_id = %s AND status = 'Registered'""",
        (event_id,),
    )["count"]
    if count >= event["max_participants"]:
        flash("This event is fully booked.", "danger")
        return redirect(url_for("events.event_detail", event_id=event_id))

    execute_insert(
        "INSERT INTO registrations (user_id, event_id, status) VALUES (%s, %s, 'Registered')",
        (user_id, event_id),
    )
    flash(f"You have successfully registered for {event['title']}!", "success")
    return redirect(url_for("events.event_detail", event_id=event_id))


@registrations_bp.route("/cancel/<int:event_id>", methods=["POST"])
@user_required
def cancel_registration(event_id):
    """Cancel the user's registration for an event."""
    user_id = session["user_id"]
    execute_query(
        """UPDATE registrations SET status = 'Cancelled'
           WHERE user_id = %s AND event_id = %s AND status = 'Registered'""",
        (user_id, event_id),
    )
    flash("Registration cancelled.", "info")
    return redirect(url_for("registrations.my_events"))


@registrations_bp.route("/my-events")
@user_required
def my_events():
    """Display all events the user is registered for."""
    user_id = session["user_id"]
    events_list = fetch_all(
        """SELECT e.*, c.name as category_name, r.registered_at, r.status as reg_status
           FROM registrations r
           JOIN events e ON r.event_id = e.id
           LEFT JOIN categories c ON e.category_id = c.id
           WHERE r.user_id = %s
           ORDER BY e.event_date DESC""",
        (user_id,),
    )
    return render_template("my_events.html", events=events_list)
