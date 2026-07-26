"""
Admin routes.
Handles admin dashboard, event management, category management, and user management.
"""

import os
import csv
import io
from functools import wraps
from datetime import date
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, send_file
)
from werkzeug.utils import secure_filename
from config import Config
from models.db import fetch_one, fetch_all, execute_query, execute_insert

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    """Decorator to restrict access to admin users only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Access denied. Admin privileges required.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    """Check if the file extension is allowed for upload."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """Display admin dashboard with statistics."""
    today = date.today().isoformat()
    stats = {
        "total_events": fetch_one("SELECT COUNT(*) as count FROM events")["count"],
        "upcoming_events": fetch_one(
            "SELECT COUNT(*) as count FROM events WHERE status = 'Upcoming'"
        )["count"],
        "completed_events": fetch_one(
            "SELECT COUNT(*) as count FROM events WHERE status = 'Completed'"
        )["count"],
        "total_users": fetch_one("SELECT COUNT(*) as count FROM users")["count"],
        "total_registrations": fetch_one(
            "SELECT COUNT(*) as count FROM registrations WHERE status = 'Registered'"
        )["count"],
    }
    popular = fetch_one(
        """SELECT e.title, COUNT(r.id) as reg_count
           FROM events e
           LEFT JOIN registrations r ON e.id = r.event_id AND r.status = 'Registered'
           GROUP BY e.id ORDER BY reg_count DESC LIMIT 1"""
    )
    stats["popular_event"] = popular["title"] if popular else "N/A"
    stats["popular_count"] = popular["reg_count"] if popular else 0

    recent_registrations = fetch_all(
        """SELECT r.*, u.name as user_name, e.title as event_title
           FROM registrations r
           JOIN users u ON r.user_id = u.id
           JOIN events e ON r.event_id = e.id
           WHERE r.status = 'Registered'
           ORDER BY r.registered_at DESC LIMIT 5"""
    )
    return render_template(
        "dashboard_admin.html", stats=stats, recent_registrations=recent_registrations
    )


# ===================== Event Management =====================

@admin_bp.route("/events")
@admin_required
def events():
    """List all events with search and filters."""
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    status = request.args.get("status", "").strip()
    page = int(request.args.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page

    query = """SELECT e.*, c.name as category_name,
               (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id AND r.status = 'Registered') as reg_count
               FROM events e
               LEFT JOIN categories c ON e.category_id = c.id WHERE 1=1"""
    params = []

    if search:
        query += " AND (e.title LIKE %s OR e.venue LIKE %s OR e.organizer LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    if category:
        query += " AND e.category_id = %s"
        params.append(category)
    if status:
        query += " AND e.status = %s"
        params.append(status)

    count_query = query.replace(
        "SELECT e.*, c.name as category_name,\n               (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id AND r.status = 'Registered') as reg_count",
        "SELECT COUNT(*) as count",
    )
    total = fetch_one(count_query, params)["count"]

    query += " ORDER BY e.event_date DESC LIMIT %s OFFSET %s"
    params.extend([per_page, offset])
    events_list = fetch_all(query, params)

    categories = fetch_all("SELECT id, name FROM categories ORDER BY name")
    total_pages = (total + per_page - 1) // per_page
    return render_template(
        "admin_events.html",
        events=events_list, categories=categories,
        search=search, category=category, status=status,
        page=page, total_pages=total_pages,
    )


@admin_bp.route("/events/add", methods=["GET", "POST"])
@admin_required
def add_event():
    """Add a new event with optional banner image upload."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category_id = request.form.get("category_id", type=int)
        event_date = request.form.get("event_date", "").strip()
        event_time = request.form.get("event_time", "").strip()
        venue = request.form.get("venue", "").strip()
        organizer = request.form.get("organizer", "").strip()
        max_participants = request.form.get("max_participants", 100, type=int)
        registration_deadline = request.form.get("registration_deadline", "").strip()

        if not title or not description or not category_id or not event_date or not event_time or not venue:
            flash("Please fill in all required fields.", "danger")
            categories = fetch_all("SELECT id, name FROM categories ORDER BY name")
            return render_template("admin_event_form.html", event=None, data=request.form, categories=categories)

        banner_filename = "default_event.png"
        if "banner_image" in request.files:
            file = request.files["banner_image"]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"event_{title[:20]}_{file.filename}")
                os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                banner_filename = filename

        execute_insert(
            """INSERT INTO events (title, description, category_id, event_date, event_time,
               venue, organizer, max_participants, registration_deadline, banner_image, created_by)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
                title, description, category_id, event_date, event_time,
                venue, organizer, max_participants, registration_deadline,
                banner_filename, session.get("user_id"),
            ),
        )
        flash("Event created successfully!", "success")
        return redirect(url_for("admin.events"))

    categories = fetch_all("SELECT id, name FROM categories ORDER BY name")
    return render_template("admin_event_form.html", event=None, data={}, categories=categories)


@admin_bp.route("/events/edit/<int:event_id>", methods=["GET", "POST"])
@admin_required
def edit_event(event_id):
    """Edit an existing event's details."""
    event = fetch_one("SELECT * FROM events WHERE id = %s", (event_id,))
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for("admin.events"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category_id = request.form.get("category_id", type=int)
        event_date = request.form.get("event_date", "").strip()
        event_time = request.form.get("event_time", "").strip()
        venue = request.form.get("venue", "").strip()
        organizer = request.form.get("organizer", "").strip()
        max_participants = request.form.get("max_participants", 100, type=int)
        registration_deadline = request.form.get("registration_deadline", "").strip()
        status = request.form.get("status", "Upcoming")

        banner_filename = event["banner_image"]
        if "banner_image" in request.files:
            file = request.files["banner_image"]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"event_{event_id}_{file.filename}")
                os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
                file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                banner_filename = filename

        execute_query(
            """UPDATE events SET title=%s, description=%s, category_id=%s, event_date=%s,
               event_time=%s, venue=%s, organizer=%s, max_participants=%s,
               registration_deadline=%s, banner_image=%s, status=%s WHERE id=%s""",
            (
                title, description, category_id, event_date, event_time,
                venue, organizer, max_participants, registration_deadline,
                banner_filename, status, event_id,
            ),
        )
        flash("Event updated successfully!", "success")
        return redirect(url_for("admin.events"))

    categories = fetch_all("SELECT id, name FROM categories ORDER BY name")
    return render_template("admin_event_form.html", event=event, data=event, categories=categories)


@admin_bp.route("/events/delete/<int:event_id>", methods=["POST"])
@admin_required
def delete_event(event_id):
    """Delete an event and its associated registrations."""
    execute_query("DELETE FROM events WHERE id = %s", (event_id,))
    flash("Event deleted successfully.", "success")
    return redirect(url_for("admin.events"))


@admin_bp.route("/events/export/<int:event_id>")
@admin_required
def export_participants(event_id):
    """Export participant list for an event to CSV."""
    event = fetch_one("SELECT * FROM events WHERE id = %s", (event_id,))
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for("admin.events"))

    participants = fetch_all(
        """SELECT u.name, u.email, u.phone, u.city, r.registered_at
           FROM registrations r
           JOIN users u ON r.user_id = u.id
           WHERE r.event_id = %s AND r.status = 'Registered'
           ORDER BY r.registered_at""",
        (event_id,),
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Email", "Phone", "City", "Registered At"])
    for p in participants:
        writer.writerow([p["name"], p["email"], p["phone"], p["city"], p["registered_at"]])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"participants_{event['title'][:30]}.csv",
    )


# ===================== Category Management =====================

@admin_bp.route("/categories")
@admin_required
def categories():
    """List all categories with event counts."""
    cats = fetch_all(
        """SELECT c.*, (SELECT COUNT(*) FROM events e WHERE e.category_id = c.id) as event_count
           FROM categories c ORDER BY c.name"""
    )
    return render_template("admin_categories.html", categories=cats)


@admin_bp.route("/categories/add", methods=["POST"])
@admin_required
def add_category():
    """Add a new category."""
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    icon = request.form.get("icon", "bi-calendar-event").strip()

    if not name:
        flash("Category name is required.", "danger")
        return redirect(url_for("admin.categories"))

    existing = fetch_one("SELECT id FROM categories WHERE name = %s", (name,))
    if existing:
        flash("Category already exists.", "danger")
        return redirect(url_for("admin.categories"))

    execute_insert(
        "INSERT INTO categories (name, description, icon) VALUES (%s, %s, %s)",
        (name, description, icon),
    )
    flash("Category added successfully.", "success")
    return redirect(url_for("admin.categories"))


@admin_bp.route("/categories/delete/<int:cat_id>", methods=["POST"])
@admin_required
def delete_category(cat_id):
    """Delete a category."""
    execute_query("DELETE FROM categories WHERE id = %s", (cat_id,))
    flash("Category deleted.", "success")
    return redirect(url_for("admin.categories"))


# ===================== User Management =====================

@admin_bp.route("/users")
@admin_required
def users():
    """List all registered users with search."""
    search = request.args.get("search", "").strip()
    page = int(request.args.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page

    if search:
        users_list = fetch_all(
            """SELECT u.*, (SELECT COUNT(*) FROM registrations r WHERE r.user_id = u.id AND r.status = 'Registered') as reg_count
               FROM users u WHERE u.name LIKE %s OR u.email LIKE %s OR u.city LIKE %s
               ORDER BY u.id DESC LIMIT %s OFFSET %s""",
            (f"%{search}%", f"%{search}%", f"%{search}%", per_page, offset),
        )
        total = fetch_one(
            "SELECT COUNT(*) as count FROM users WHERE name LIKE %s OR email LIKE %s OR city LIKE %s",
            (f"%{search}%", f"%{search}%", f"%{search}%"),
        )["count"]
    else:
        users_list = fetch_all(
            """SELECT u.*, (SELECT COUNT(*) FROM registrations r WHERE r.user_id = u.id AND r.status = 'Registered') as reg_count
               FROM users u ORDER BY u.id DESC LIMIT %s OFFSET %s""",
            (per_page, offset),
        )
        total = fetch_one("SELECT COUNT(*) as count FROM users")["count"]

    total_pages = (total + per_page - 1) // per_page
    return render_template(
        "admin_users.html",
        users=users_list, search=search,
        page=page, total_pages=total_pages,
    )
