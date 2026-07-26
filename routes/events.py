"""
Events routes.
Handles public event browsing and event detail views.
"""

from flask import Blueprint, render_template, request
from models.db import fetch_one, fetch_all

events_bp = Blueprint("events", __name__)


@events_bp.route("/events")
def list_events():
    """List all upcoming events with search, category filter, and pagination."""
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    page = int(request.args.get("page", 1))
    per_page = 9
    offset = (page - 1) * per_page

    query = """SELECT e.*, c.name as category_name, c.icon as category_icon,
               (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id AND r.status = 'Registered') as reg_count
               FROM events e
               LEFT JOIN categories c ON e.category_id = c.id
               WHERE e.status = 'Upcoming'"""
    params = []

    if search:
        query += " AND (e.title LIKE %s OR e.venue LIKE %s OR e.description LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    if category:
        query += " AND e.category_id = %s"
        params.append(category)

    count_query = query.replace(
        "SELECT e.*, c.name as category_name, c.icon as category_icon,\n               (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id AND r.status = 'Registered') as reg_count",
        "SELECT COUNT(*) as count",
    )
    total = fetch_one(count_query, params)["count"]

    query += " ORDER BY e.event_date ASC LIMIT %s OFFSET %s"
    params.extend([per_page, offset])
    events_list = fetch_all(query, params)

    categories = fetch_all("SELECT id, name, icon FROM categories ORDER BY name")
    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "events.html",
        events=events_list, categories=categories,
        search=search, category=category,
        page=page, total_pages=total_pages,
    )


@events_bp.route("/events/<int:event_id>")
def event_detail(event_id):
    """Display detailed information about a specific event."""
    event = fetch_one(
        """SELECT e.*, c.name as category_name, c.icon as category_icon,
           (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id AND r.status = 'Registered') as reg_count
           FROM events e
           LEFT JOIN categories c ON e.category_id = c.id
           WHERE e.id = %s""",
        (event_id,),
    )
    if not event:
        return render_template("404.html"), 404

    is_registered = False
    from flask import session
    if session.get("role") == "user":
        reg = fetch_one(
            """SELECT id FROM registrations
               WHERE user_id = %s AND event_id = %s AND status = 'Registered'""",
            (session["user_id"], event_id),
        )
        is_registered = reg is not None

    return render_template("event_detail.html", event=event, is_registered=is_registered)
