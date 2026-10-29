import os
import sqlite3
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "trackify.db")

app = FastAPI(
    title="Trackify REST API",
    description="Enterprise Software Bug & Issue Tracker Backend Engine",
    version="2.0.0"
)

# Enable CORS for all frontends (Render static sites, localhost, Vercel, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'tester',
        full_name TEXT
    )
    """)

    # 2. Projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        start_date TEXT,
        status TEXT NOT NULL DEFAULT 'active'
    )
    """)

    # 3. Tickets Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT NOT NULL DEFAULT 'medium',
        status TEXT NOT NULL DEFAULT 'open',
        project_id INTEGER NOT NULL,
        creator_id INTEGER NOT NULL,
        assigned_dev_id INTEGER,
        created_at TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id),
        FOREIGN KEY (creator_id) REFERENCES users(id),
        FOREIGN KEY (assigned_dev_id) REFERENCES users(id)
    )
    """)

    # 4. Comments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT,
        FOREIGN KEY (ticket_id) REFERENCES tickets(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Seed initial demo data if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES ('admin', 'admin123', 'admin', 'System Administrator')")
        cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES ('rahul_dev', 'admin123', 'developer', 'Rahul Sharma (Dev Lead)')")
        cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES ('sneha_qa', 'admin123', 'tester', 'Sneha Patel (QA Engineer)')")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_short = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("INSERT INTO projects (name, description, start_date, status) VALUES ('E-Commerce Cloud Microservices', 'Microservices backend for payment processing, cart checkout, and inventory sync.', ?, 'active')", (date_short,))
        cursor.execute("INSERT INTO projects (name, description, start_date, status) VALUES ('College Mobile App v2', 'Cross-platform flutter application for student attendance, timetable, and campus alerts.', ?, 'active')", (date_short,))
        cursor.execute("INSERT INTO projects (name, description, start_date, status) VALUES ('DevOps CI/CD Automation Pipeline', 'Containerized Docker pipeline, test automation harness, and production deployer.', ?, 'completed')", (date_short,))

        cursor.execute("""
        INSERT INTO tickets (title, description, priority, status, project_id, creator_id, assigned_dev_id, created_at)
        VALUES ('High memory spike on checkout endpoint under concurrent load', 'Stress tests revealed that handling 500+ requests/sec causes thread pool exhaustion and 504 Gateway Timeouts.', 'high', 'in_progress', 1, 3, 2, ?)
        """, (now,))

        cursor.execute("""
        INSERT INTO tickets (title, description, priority, status, project_id, creator_id, assigned_dev_id, created_at)
        VALUES ('OAuth Google Sign-in fails on Android 14 devices', 'Users on newer Android versions report NullPointerException during authorization callback redirect.', 'high', 'open', 2, 3, NULL, ?)
        """, (now,))

        cursor.execute("""
        INSERT INTO tickets (title, description, priority, status, project_id, creator_id, assigned_dev_id, created_at)
        VALUES ('Push notification token expired exception in background service', 'FCM registration tokens are not being refreshed automatically when app runs in background battery saver mode.', 'medium', 'in_progress', 2, 1, 2, ?)
        """, (now,))

        cursor.execute("""
        INSERT INTO tickets (title, description, priority, status, project_id, creator_id, assigned_dev_id, created_at)
        VALUES ('Broken pagination on order history data table', 'Clicking page 2 in order summary table resets the date filters. Query parameters need to be preserved.', 'low', 'resolved', 1, 3, 2, ?)
        """, (now,))

        cursor.execute("""
        INSERT INTO comments (ticket_id, user_id, content, created_at)
        VALUES (1, 2, 'Identified connection pool leak in Redis connector. Patch applied and under load testing.', ?)
        """, (now,))

    conn.commit()
    conn.close()

# Initialize DB on import
init_db()

# --- Pydantic Request Models ---
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = 'tester'
    full_name: Optional[str] = None

class ProjectCreateRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    status: str = "active"

class TicketCreateRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: str = "medium"
    project_id: int
    creator_id: int
    assigned_dev_id: Optional[int] = None

class TicketUpdateRequest(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_dev_id: Optional[int] = None

class CommentCreateRequest(BaseModel):
    user_id: int
    content: str


# --- API Endpoints ---

@app.get("/")
def root():
    return {
        "app": "Trackify REST API",
        "status": "online",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "message": "Trackify FastAPI Backend is Active & Awake",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/auth/login")
def login(req: LoginRequest, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, username, role, full_name FROM users WHERE username = ? AND password = ?", (req.username.strip(), req.password.strip()))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "full_name": user["full_name"] or user["username"]
    }

@app.post("/api/auth/register")
def register(req: RegisterRequest, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                       (req.username.strip(), req.password.strip(), req.role.strip(), req.full_name or req.username.strip()))
        db.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "username": req.username, "role": req.role, "message": "User registered successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")

@app.get("/api/dashboard/stats")
def dashboard_stats(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets")
    total_tickets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'in_progress' OR status = 'open'")
    in_progress_tickets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE status = 'resolved'")
    resolved_tickets = cursor.fetchone()[0]

    # Recent tickets
    cursor.execute("""
    SELECT t.id, t.title, t.priority, t.status, t.created_at, p.name as project_name, u.username as dev_username
    FROM tickets t
    JOIN projects p ON t.project_id = p.id
    LEFT JOIN users u ON t.assigned_dev_id = u.id
    ORDER BY t.id DESC LIMIT 6
    """)
    recent_tickets = [dict(row) for row in cursor.fetchall()]

    # Projects overview
    cursor.execute("""
    SELECT p.id, p.name, p.description, p.status, p.start_date, COUNT(t.id) as ticket_count
    FROM projects p
    LEFT JOIN tickets t ON p.id = t.project_id
    GROUP BY p.id
    ORDER BY p.id DESC LIMIT 6
    """)
    projects = [dict(row) for row in cursor.fetchall()]

    return {
        "total_projects": total_projects,
        "total_tickets": total_tickets,
        "in_progress_tickets": in_progress_tickets,
        "resolved_tickets": resolved_tickets,
        "recent_tickets": recent_tickets,
        "projects": projects
    }

@app.get("/api/projects")
def list_projects(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
    SELECT p.id, p.name, p.description, p.status, p.start_date, COUNT(t.id) as ticket_count
    FROM projects p
    LEFT JOIN tickets t ON p.id = t.project_id
    GROUP BY p.id
    ORDER BY p.id DESC
    """)
    return [dict(row) for row in cursor.fetchall()]

@app.post("/api/projects")
def create_project(req: ProjectCreateRequest, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO projects (name, description, start_date, status) VALUES (?, ?, ?, ?)",
                   (req.name, req.description, date_str, req.status))
    db.commit()
    return {"id": cursor.lastrowid, "message": "Project created successfully"}

@app.get("/api/tickets")
def list_tickets(project_id: Optional[int] = None, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    if project_id:
        cursor.execute("""
        SELECT t.id, t.title, t.description, t.priority, t.status, t.created_at, p.name as project_name, 
               u_dev.username as dev_username, u_cr.username as creator_username
        FROM tickets t
        JOIN projects p ON t.project_id = p.id
        JOIN users u_cr ON t.creator_id = u_cr.id
        LEFT JOIN users u_dev ON t.assigned_dev_id = u_dev.id
        WHERE t.project_id = ?
        ORDER BY t.id DESC
        """, (project_id,))
    else:
        cursor.execute("""
        SELECT t.id, t.title, t.description, t.priority, t.status, t.created_at, p.name as project_name, 
               u_dev.username as dev_username, u_cr.username as creator_username
        FROM tickets t
        JOIN projects p ON t.project_id = p.id
        JOIN users u_cr ON t.creator_id = u_cr.id
        LEFT JOIN users u_dev ON t.assigned_dev_id = u_dev.id
        ORDER BY t.id DESC
        """)
    return [dict(row) for row in cursor.fetchall()]

@app.post("/api/tickets")
def create_ticket(req: TicketCreateRequest, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO tickets (title, description, priority, status, project_id, creator_id, assigned_dev_id, created_at)
    VALUES (?, ?, ?, 'open', ?, ?, ?, ?)
    """, (req.title, req.description, req.priority, req.project_id, req.creator_id, req.assigned_dev_id, now))
    db.commit()
    return {"id": cursor.lastrowid, "message": "Ticket created successfully"}

@app.get("/api/tickets/{ticket_id}")
def get_ticket(ticket_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
    SELECT t.id, t.title, t.description, t.priority, t.status, t.created_at, t.project_id, t.assigned_dev_id,
           p.name as project_name, u_dev.username as dev_username, u_cr.username as creator_username
    FROM tickets t
    JOIN projects p ON t.project_id = p.id
    JOIN users u_cr ON t.creator_id = u_cr.id
    LEFT JOIN users u_dev ON t.assigned_dev_id = u_dev.id
    WHERE t.id = ?
    """, (ticket_id,))
    ticket = cursor.fetchone()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Fetch comments
    cursor.execute("""
    SELECT c.id, c.content, c.created_at, u.username, u.role
    FROM comments c
    JOIN users u ON c.user_id = u.id
    WHERE c.ticket_id = ?
    ORDER BY c.id ASC
    """, (ticket_id,))
    comments = [dict(row) for row in cursor.fetchall()]

    result = dict(ticket)
    result["comments"] = comments
    return result

@app.patch("/api/tickets/{ticket_id}")
def update_ticket(ticket_id: int, req: TicketUpdateRequest, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    updates = []
    params = []
    if req.status:
        updates.append("status = ?")
        params.append(req.status)
    if req.priority:
        updates.append("priority = ?")
        params.append(req.priority)
    if req.assigned_dev_id is not None:
        updates.append("assigned_dev_id = ?")
        params.append(req.assigned_dev_id)

    if not updates:
        return {"message": "No updates provided"}

    params.append(ticket_id)
    query = f"UPDATE tickets SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, tuple(params))
    db.commit()
    return {"message": "Ticket updated successfully"}

@app.post("/api/tickets/{ticket_id}/comments")
def add_comment(ticket_id: int, req: CommentCreateRequest, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO comments (ticket_id, user_id, content, created_at) VALUES (?, ?, ?, ?)",
                   (ticket_id, req.user_id, req.content, now))
    db.commit()
    return {"id": cursor.lastrowid, "message": "Comment posted successfully"}

@app.get("/api/developers")
def get_developers(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, username, full_name FROM users WHERE role = 'developer'")
    return [dict(row) for row in cursor.fetchall()]
