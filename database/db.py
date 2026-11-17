"""
HireLens AI - SQLite Database Interface
Handles users, authentication, jobs database, notifications, and saved resumes.
"""
import sqlite3
import hashlib
import os
import json
from datetime import datetime
from config import DB_PATH

def get_connection():
    """Establish and return SQLite connection with high-performance PRAGMAs."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA cache_size = 10000")
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Hashes a password with salt using SHA-256."""
    if not salt:
        salt = os.urandom(16).hex()
    salted = f"{salt}:{password}".encode("utf-8")
    pwd_hash = hashlib.sha256(salted).hexdigest()
    return pwd_hash, salt

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verifies that the provided password matches the stored hash."""
    expected_hash, _ = hash_password(password, salt)
    return expected_hash == stored_hash

def init_db():
    """Initialize database tables and indexes."""
    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        full_name TEXT NOT NULL,
        phone TEXT,
        city TEXT,
        state TEXT,
        country TEXT,
        latitude REAL,
        longitude REAL,
        target_role TEXT,
        target_category TEXT,
        skills TEXT,
        experience_level TEXT,
        notifications_enabled INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    )
    """)

    # Jobs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        category TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        country TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        salary_range TEXT,
        job_type TEXT,
        experience_required TEXT,
        required_skills TEXT,
        description TEXT,
        posted_date TEXT NOT NULL,
        source TEXT DEFAULT 'HireLens Direct'
    )
    """)

    # Notifications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        job_id INTEGER,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        matched_skills TEXT,
        is_read INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (job_id) REFERENCES jobs (id)
    )
    """)

    # User Saved Resumes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resume_name TEXT NOT NULL,
        resume_data_json TEXT NOT NULL,
        ats_score REAL,
        target_category TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()
    conn.close()

# ==================== User Functions ====================

def register_user(username, email, password, full_name, phone="", city="", state="", country="",
                  target_role="", target_category="INFORMATION-TECHNOLOGY", skills="", experience_level="Student/Fresher",
                  lat=0.0, lon=0.0):
    """Registers a new user into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    pwd_hash, salt = hash_password(password)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
        INSERT INTO users (
            username, email, password_hash, salt, full_name, phone,
            city, state, country, latitude, longitude,
            target_role, target_category, skills, experience_level,
            notifications_enabled, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
        """, (username, email, pwd_hash, salt, full_name, phone,
              city, state, country, lat, lon,
              target_role, target_category, skills, experience_level, now))
        conn.commit()
        user_id = cursor.lastrowid
        return {"success": True, "user_id": user_id, "message": "Registration successful!"}
    except sqlite3.IntegrityError as e:
        err = str(e).lower()
        if "username" in err:
            return {"success": False, "message": "Username already exists. Please pick another."}
        elif "email" in err:
            return {"success": False, "message": "Email address already registered. Please log in."}
        return {"success": False, "message": f"Database integrity error: {e}"}
    finally:
        conn.close()

def authenticate_user(login_identifier, password):
    """Authenticates by username or email. Returns user dict or None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users WHERE username = ? OR email = ?
    """, (login_identifier, login_identifier))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return None

    if verify_password(password, user["password_hash"], user["salt"]):
        return dict(user)
    return None

def get_user_by_id(user_id):
    """Returns user profile dictionary."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def update_user_profile(user_id, **kwargs):
    """Updates user fields dynamically."""
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    for k, v in kwargs.items():
        fields.append(f"{k} = ?")
        values.append(v)
    values.append(user_id)

    query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return True

# ==================== Jobs Functions ====================

def insert_job(title, company, category, city, state, country, lat, lon,
               salary_range, job_type, experience_required, required_skills, description,
               posted_date=None, source="HireLens Direct"):
    """Inserts a new job opening."""
    conn = get_connection()
    cursor = conn.cursor()
    if not posted_date:
        posted_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    INSERT INTO jobs (
        title, company, category, city, state, country, latitude, longitude,
        salary_range, job_type, experience_required, required_skills, description,
        posted_date, source
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, company, category, city, state, country, lat, lon,
          salary_range, job_type, experience_required, required_skills, description,
          posted_date, source))
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()
    return job_id

def get_all_jobs(category=None, country=None, state=None, city=None, search=None, limit=200):
    """Queries jobs with optional filters."""
    conn = get_connection()
    cursor = conn.cursor()
    conditions = []
    params = []

    if category and category != "All":
        conditions.append("category = ?")
        params.append(category)
    if country and country != "All":
        conditions.append("country = ?")
        params.append(country)
    if state and state != "All":
        conditions.append("LOWER(state) = LOWER(?)")
        params.append(state)
    if city and city != "All":
        conditions.append("LOWER(city) = LOWER(?)")
        params.append(city)
    if search:
        search_like = f"%{search.lower()}%"
        conditions.append("(LOWER(title) LIKE ? OR LOWER(company) LIKE ? OR LOWER(required_skills) LIKE ? OR LOWER(description) LIKE ?)")
        params.extend([search_like, search_like, search_like, search_like])

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"SELECT * FROM jobs {where_clause} ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_jobs_near_user(city, state, country, category=None):
    """Retrieves jobs prioritizing same city/state/country."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Priority 1: Exact city match
    city_jobs = []
    if city:
        cursor.execute("""
        SELECT *, 1 as match_priority FROM jobs 
        WHERE LOWER(city) = LOWER(?)
        ORDER BY id DESC LIMIT 50
        """, (city.strip(),))
        city_jobs = [dict(r) for r in cursor.fetchall()]

    # Priority 2: Same state
    state_jobs = []
    if state:
        cursor.execute("""
        SELECT *, 2 as match_priority FROM jobs 
        WHERE LOWER(state) = LOWER(?) AND LOWER(city) != LOWER(?)
        ORDER BY id DESC LIMIT 50
        """, (state.strip(), city.strip() if city else ""))
        state_jobs = [dict(r) for r in cursor.fetchall()]

    # Priority 3: Same country or Remote
    country_jobs = []
    if country:
        cursor.execute("""
        SELECT *, 3 as match_priority FROM jobs 
        WHERE (LOWER(country) = LOWER(?) OR job_type = 'Remote') 
        AND LOWER(state) != LOWER(?)
        ORDER BY id DESC LIMIT 50
        """, (country.strip(), state.strip() if state else ""))
        country_jobs = [dict(r) for r in cursor.fetchall()]

    conn.close()
    
    # Combine and de-duplicate by ID
    combined = []
    seen = set()
    for j in city_jobs + state_jobs + country_jobs:
        if j["id"] not in seen:
            seen.add(j["id"])
            combined.append(j)
    return combined

# ==================== Notifications Functions ====================

def create_notification(user_id, title, message, job_id=None, matched_skills=""):
    """Inserts a new notification for a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO notifications (user_id, job_id, title, message, matched_skills, is_read, created_at)
    VALUES (?, ?, ?, ?, ?, 0, ?)
    """, (user_id, job_id, title, message, matched_skills, now))
    conn.commit()
    notif_id = cursor.lastrowid
    conn.close()
    return notif_id

def get_user_notifications(user_id, limit=20):
    """Retrieves notifications for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT n.*, j.title as job_title, j.company as job_company, j.city as job_city
    FROM notifications n
    LEFT JOIN jobs j ON n.job_id = j.id
    WHERE n.user_id = ?
    ORDER BY n.id DESC LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def mark_notification_read(notif_id):
    """Marks a notification as read."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
    conn.commit()
    conn.close()

def mark_all_notifications_read(user_id):
    """Marks all user notifications as read."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# ==================== Resume Persistence Functions ====================

def save_user_resume(user_id, resume_name, resume_data_dict, ats_score=None, category=None):
    """Saves generated or parsed resume json for the user."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO user_resumes (user_id, resume_name, resume_data_json, ats_score, target_category, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, resume_name, json.dumps(resume_data_dict), ats_score, category, now))
    conn.commit()
    resume_id = cursor.lastrowid
    conn.close()
    return resume_id

def get_user_resumes(user_id):
    """Retrieves all saved resumes for the user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM user_resumes WHERE user_id = ? ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    resumes = []
    for r in rows:
        d = dict(r)
        try:
            d["data"] = json.loads(d["resume_data_json"])
        except Exception:
            d["data"] = {}
        resumes.append(d)
    return resumes
