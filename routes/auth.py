"""
Authentication routes.
Handles login, logout, registration, and session management.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.db import fetch_one, execute_insert

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET"])
def landing():
    """Display the public landing page."""
    if "role" in session:
        return redirect(url_for(get_redirect_url(session["role"])))
    return render_template("landing.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Display login page and handle authentication."""
    if "role" in session:
        return redirect(url_for(get_redirect_url(session["role"])))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "").strip()

        if not email or not password or not role:
            flash("All fields are required.", "danger")
            return render_template("login.html")

        user = None
        if role == "admin":
            user = fetch_one(
                "SELECT * FROM admins WHERE email = %s AND password = %s",
                (email, password),
            )
        elif role == "user":
            user = fetch_one(
                "SELECT * FROM users WHERE email = %s AND password = %s",
                (email, password),
            )

        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            session["role"] = role
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for(get_redirect_url(role)))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Display registration form and handle new user registration."""
    if "role" in session:
        return redirect(url_for(get_redirect_url(session["role"])))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        phone = request.form.get("phone", "").strip()
        city = request.form.get("city", "").strip()

        if not name or not email or not password:
            flash("Name, email, and password are required.", "danger")
            return render_template("register.html", data=request.form)

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html", data=request.form)

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("register.html", data=request.form)

        existing = fetch_one("SELECT id FROM users WHERE email = %s", (email,))
        if existing:
            flash("Email already registered. Please login.", "danger")
            return render_template("register.html", data=request.form)

        execute_insert(
            "INSERT INTO users (name, email, password, phone, city) VALUES (%s, %s, %s, %s, %s)",
            (name, email, password, phone, city),
        )
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", data={})


@auth_bp.route("/logout")
def logout():
    """Clear session and redirect to landing page."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.landing"))


def get_redirect_url(role):
    """Return the appropriate dashboard URL based on user role."""
    urls = {
        "admin": "admin.dashboard",
        "user": "user.dashboard",
    }
    return urls.get(role, "auth.login")
