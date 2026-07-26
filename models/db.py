"""
Database connection and query helper module.
Supports MySQL when configured, falls back to SQLite automatically.
"""

import os
import sqlite3
import pymysql
from config import Config

USE_SQLITE = not os.environ.get("DB_HOST")


def _get_db_path():
    """Return the SQLite database file path."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "event.db")


def get_connection():
    """Create and return a database connection (MySQL or SQLite)."""
    if USE_SQLITE:
        db_path = _get_db_path()
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def _convert_params(query, params):
    """Convert MySQL %s placeholders to SQLite ? placeholders."""
    if USE_SQLITE and params:
        query = query.replace("%s", "?")
    return query, params


def _rows_to_dicts(rows):
    """Convert sqlite3.Row objects to plain dicts."""
    if rows is None:
        return None
    if isinstance(rows, sqlite3.Row):
        return dict(rows)
    if isinstance(rows, list):
        return [dict(r) if isinstance(r, sqlite3.Row) else r for r in rows]
    return rows


def fetch_one(query, params=None):
    """Execute a query and return a single row as a dictionary."""
    query, params = _convert_params(query, params)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        return _rows_to_dicts(result)
    finally:
        conn.close()


def fetch_all(query, params=None):
    """Execute a query and return all rows as a list of dictionaries."""
    query, params = _convert_params(query, params)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return _rows_to_dicts(result)
    finally:
        conn.close()


def execute_query(query, params=None):
    """Execute an INSERT, UPDATE, or DELETE query and return affected rows."""
    query, params = _convert_params(query, params)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def execute_insert(query, params=None):
    """Execute an INSERT query and return the last inserted ID."""
    query, params = _convert_params(query, params)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def init_sqlite_db():
    """Create tables and seed data for SQLite on first run."""
    if not USE_SQLITE:
        return

    db_path = _get_db_path()
    if os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        phone TEXT,
        city TEXT,
        bio TEXT,
        profile_pic TEXT DEFAULT 'default.png',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        icon TEXT DEFAULT 'bi-calendar-event',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        event_date DATE NOT NULL,
        event_time TIME NOT NULL,
        venue TEXT NOT NULL,
        organizer TEXT NOT NULL,
        max_participants INTEGER DEFAULT 100,
        registration_deadline DATE NOT NULL,
        banner_image TEXT DEFAULT 'default_event.png',
        status TEXT DEFAULT 'Upcoming',
        created_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
        FOREIGN KEY (created_by) REFERENCES admins(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        event_id INTEGER NOT NULL,
        status TEXT DEFAULT 'Registered',
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, event_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_events_date ON events(event_date);
    CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
    CREATE INDEX IF NOT EXISTS idx_events_category ON events(category_id);
    CREATE INDEX IF NOT EXISTS idx_registrations_user ON registrations(user_id);
    CREATE INDEX IF NOT EXISTS idx_registrations_event ON registrations(event_id);
    """)

    from datetime import date, timedelta
    today = date.today().isoformat()

    cur.executemany("INSERT INTO admins (name, email, password, phone) VALUES (?,?,?,?)",
        [("System Admin", "admin@events.com", "admin123", "9876543210")])

    cur.executemany("INSERT INTO users (name, email, password, phone, city, bio) VALUES (?,?,?,?,?,?)",
        [
            ("John Doe", "john@email.com", "user123", "9876543211", "Mumbai", "Software enthusiast and event lover."),
            ("Jane Smith", "jane@email.com", "user123", "9876543212", "Delhi", "Full-stack developer and tech speaker."),
            ("Alex Johnson", "alex@email.com", "user123", "9876543213", "Bangalore", "UI/UX designer and creative thinker."),
            ("Priya Patel", "priya@email.com", "user123", "9876543214", "Ahmedabad", "Data science enthusiast and blogger."),
            ("Rahul Verma", "rahul@email.com", "user123", "9876543215", "Pune", "Cloud computing and DevOps explorer."),
            ("Sneha Reddy", "sneha@email.com", "user123", "9876543216", "Hyderabad", "Machine learning student."),
            ("Amit Singh", "amit@email.com", "user123", "9876543217", "Jaipur", "Mobile app developer."),
            ("Neha Gupta", "neha@email.com", "user123", "9876543218", "Lucknow", "Cybersecurity enthusiast."),
        ])

    cur.executemany("INSERT INTO categories (name, description, icon) VALUES (?,?,?)",
        [
            ("Technology", "Events related to technology and innovation", "bi-laptop"),
            ("Workshop", "Hands-on learning sessions and workshops", "bi-tools"),
            ("Seminar", "Educational talks and knowledge-sharing", "bi-mic"),
            ("Cultural", "Cultural festivals and celebrations", "bi-music-note"),
            ("Sports", "Sports tournaments and competitions", "bi-trophy"),
            ("Networking", "Professional networking events", "bi-people"),
            ("Hackathon", "Coding competitions and challenges", "bi-code-slash"),
            ("Conference", "Industry conferences and summits", "bi-easel"),
        ])

    cur.executemany("INSERT INTO events (title, description, category_id, event_date, event_time, venue, organizer, max_participants, registration_deadline, status, created_by) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        [
            ("Tech Summit 2026", "Annual technology summit featuring industry leaders.", 1, f"{(date.today()+timedelta(days=15)).isoformat()}", "09:00:00", "Main Auditorium, Tech University", "Tech University", 500, f"{(date.today()+timedelta(days=10)).isoformat()}", "Upcoming", 1),
            ("Python Workshop for Beginners", "Hands-on workshop covering Python fundamentals.", 2, f"{(date.today()+timedelta(days=7)).isoformat()}", "10:00:00", "Lab 3, CS Building", "Code Academy", 60, f"{(date.today()+timedelta(days=5)).isoformat()}", "Upcoming", 1),
            ("AI & ML Seminar", "Expert-led seminar on AI and machine learning.", 3, f"{(date.today()+timedelta(days=20)).isoformat()}", "14:00:00", "Seminar Hall B, Engineering Block", "AI Research Lab", 200, f"{(date.today()+timedelta(days=18)).isoformat()}", "Upcoming", 1),
            ("Annual Cultural Fest - Spectrum", "Three-day cultural festival with music, dance, and drama.", 4, f"{(date.today()+timedelta(days=30)).isoformat()}", "16:00:00", "Open Air Theatre, Main Campus", "Cultural Committee", 1000, f"{(date.today()+timedelta(days=25)).isoformat()}", "Upcoming", 1),
            ("Inter-College Cricket Tournament", "Cricket tournament between engineering colleges.", 5, f"{(date.today()+timedelta(days=25)).isoformat()}", "07:00:00", "Sports Complex", "Sports Committee", 200, f"{(date.today()+timedelta(days=20)).isoformat()}", "Upcoming", 1),
            ("Career Connect Networking", "Networking event with alumni and recruiters.", 6, f"{(date.today()+timedelta(days=12)).isoformat()}", "11:00:00", "Conference Room A", "Placement Cell", 150, f"{(date.today()+timedelta(days=10)).isoformat()}", "Upcoming", 1),
            ("48-Hour Hackathon - CodeStorm", "Intense hackathon with prizes worth Rs. 1 Lakh.", 7, f"{(date.today()+timedelta(days=18)).isoformat()}", "10:00:00", "Innovation Hub, Tech Park", "Innovation Cell", 120, f"{(date.today()+timedelta(days=16)).isoformat()}", "Upcoming", 1),
            ("International Tech Conference", "Global conference with researchers and industry leaders.", 8, f"{(date.today()+timedelta(days=45)).isoformat()}", "09:00:00", "Convention Center", "Global Tech Association", 800, f"{(date.today()+timedelta(days=40)).isoformat()}", "Upcoming", 1),
            ("Web Development Bootcamp", "Intensive 5-day bootcamp on web technologies.", 2, f"{(date.today()-timedelta(days=10)).isoformat()}", "10:00:00", "Lab 5, CS Building", "Code Academy", 40, f"{(date.today()-timedelta(days=15)).isoformat()}", "Completed", 1),
            ("Startup Meetup 2025", "Monthly meetup for entrepreneurs and founders.", 6, f"{(date.today()-timedelta(days=30)).isoformat()}", "18:00:00", "Cafe Innovation", "Startup Cell", 80, f"{(date.today()-timedelta(days=35)).isoformat()}", "Completed", 1),
        ])

    cur.executemany("INSERT INTO registrations (user_id, event_id, status) VALUES (?,?,?)",
        [
            (1, 1, "Registered"), (1, 2, "Registered"), (1, 7, "Registered"),
            (2, 1, "Registered"), (2, 3, "Registered"), (2, 6, "Registered"),
            (3, 1, "Registered"), (3, 4, "Registered"), (3, 5, "Registered"),
            (4, 2, "Registered"), (4, 3, "Registered"),
            (5, 1, "Registered"), (5, 7, "Registered"), (5, 8, "Registered"),
            (6, 3, "Registered"), (6, 6, "Registered"),
            (7, 4, "Registered"), (7, 5, "Registered"),
            (8, 1, "Registered"), (8, 2, "Registered"),
            (1, 9, "Registered"), (2, 9, "Registered"),
            (3, 10, "Registered"), (4, 10, "Registered"),
        ])

    conn.commit()
    conn.close()
