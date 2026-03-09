"""Flask Task Management Application - POC with raw SQL."""

import sqlite3
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database import (
    DB_PATH,
    TASK_STATUSES,
    get_connection,
    get_connection_with_row_factory,
    init_db,
)

app = Flask(__name__)
app.secret_key = "taskman-poc-secret-key-change-in-production"
app.config["DATABASE"] = str(DB_PATH)

# Initialize database on first import (creates tables if missing)
init_db()


def login_required(f):
    """Decorator to require login for a route."""

    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated


def get_current_user():
    """Return the current logged-in user row or None."""
    if "user_id" not in session:
        return None
    conn = get_connection_with_row_factory()
    try:
        cur = conn.execute(
            "SELECT id, username FROM users WHERE id = ?", (session["user_id"],)
        )
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_all_users():
    """Return all users for assignment dropdown."""
    conn = get_connection_with_row_factory()
    try:
        cur = conn.execute("SELECT id, username FROM users ORDER BY username")
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


@app.route("/")
def index():
    """Main view: list all tasks with optional filtering."""
    if "user_id" not in session:
        return redirect(url_for("login"))
    status_filter = request.args.get("status", "")
    user_filter = request.args.get("assigned_to", "")
    conn = get_connection_with_row_factory()
    try:
        query = """
            SELECT t.id, t.title, t.description, t.status, t.assigned_to,
                   t.created_at, t.created_by,
                   u1.username AS assigned_to_username,
                   u2.username AS created_by_username
            FROM tasks t
            LEFT JOIN users u1 ON t.assigned_to = u1.id
            LEFT JOIN users u2 ON t.created_by = u2.id
            WHERE 1=1
        """
        params = []
        if status_filter:
            query += " AND t.status = ?"
            params.append(status_filter)
        if user_filter:
            query += " AND t.assigned_to = ?"
            params.append(user_filter)
        query += " ORDER BY t.updated_at DESC"
        cur = conn.execute(query, params)
        tasks = [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()
    users = get_all_users()
    return render_template(
        "index.html",
        tasks=tasks,
        users=users,
        statuses=TASK_STATUSES,
        status_filter=status_filter,
        user_filter=user_filter,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template("register.html")
        conn = get_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()
            flash(f"Username '{username}' is already taken.", "error")
            return render_template("register.html")
        finally:
            conn.close()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login with username/password (plain-text)."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template("login.html")
        conn = get_connection_with_row_factory()
        try:
            cur = conn.execute(
                "SELECT id, username, password FROM users WHERE username = ?",
                (username,),
            )
            row = cur.fetchone()
            if row and row["password"] == password:
                session["user_id"] = row["id"]
                session["username"] = row["username"]
                flash(f"Welcome, {row['username']}!", "success")
                return redirect(url_for("index"))
        finally:
            conn.close()
        flash("Invalid username or password.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Logout and clear session."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/task/new", methods=["GET", "POST"])
@login_required
def task_new():
    """Create a new task."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "draft")
        assigned_to = request.form.get("assigned_to") or None
        if not title:
            flash("Title is required.", "error")
            return render_task_form(status=status, assigned_to=assigned_to)
        if status not in TASK_STATUSES:
            status = "draft"
        if assigned_to:
            try:
                assigned_to = int(assigned_to)
            except ValueError:
                assigned_to = None
        conn = get_connection()
        try:
            cur = conn.execute(
                """INSERT INTO tasks (title, description, status, assigned_to, created_by)
                   VALUES (?, ?, ?, ?, ?)""",
                (title, description, status, assigned_to, session["user_id"]),
            )
            task_id = cur.lastrowid
            conn.execute(
                """INSERT INTO taskslog (task_id, action, changed_by, new_value)
                   VALUES (?, ?, ?, ?)""",
                (task_id, "created", session["user_id"], f"Task created: {title}"),
            )
            conn.commit()
            flash("Task created successfully.", "success")
            return redirect(url_for("index"))
        finally:
            conn.close()

    return render_task_form()


def render_task_form(task=None, status="draft", assigned_to=None):
    """Helper to render task create/edit form."""
    users = get_all_users()
    return render_template(
        "task_form.html",
        task=task,
        users=users,
        statuses=TASK_STATUSES,
        default_status=status,
        default_assigned_to=assigned_to,
    )


@app.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def task_edit(task_id):
    """Edit an existing task."""
    conn = get_connection_with_row_factory()
    try:
        cur = conn.execute(
            "SELECT id, title, description, status, assigned_to, created_by FROM tasks WHERE id = ?",
            (task_id,),
        )
        task = cur.fetchone()
        if not task:
            flash("Task not found.", "error")
            return redirect(url_for("index"))
        task = dict(task)
    finally:
        conn.close()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        status = request.form.get("status", "draft")
        assigned_to = request.form.get("assigned_to") or None
        if not title:
            flash("Title is required.", "error")
            return render_task_form(task=task, status=status, assigned_to=assigned_to)
        if status not in TASK_STATUSES:
            status = task["status"]
        if assigned_to:
            try:
                assigned_to = int(assigned_to)
            except ValueError:
                assigned_to = task.get("assigned_to")
        conn = get_connection()
        try:
            old_status = task["status"]
            old_assigned = task.get("assigned_to")
            conn.execute(
                """UPDATE tasks SET title=?, description=?, status=?, assigned_to=?,
                   updated_at=CURRENT_TIMESTAMP WHERE id=?""",
                (title, description, status, assigned_to, task_id),
            )
            logs = []
            if old_status != status:
                logs.append((task_id, "status_change", session["user_id"], old_status, status))
            if old_assigned != assigned_to:
                logs.append((task_id, "assign_change", session["user_id"], str(old_assigned or ""), str(assigned_to or "")))
            for log in logs:
                conn.execute(
                    "INSERT INTO taskslog (task_id, action, changed_by, old_value, new_value) VALUES (?, ?, ?, ?, ?)",
                    log,
                )
            conn.commit()
            flash("Task updated successfully.", "success")
            return redirect(url_for("index"))
        finally:
            conn.close()

    return render_task_form(
        task=task,
        status=task["status"],
        assigned_to=task.get("assigned_to"),
    )


@app.route("/task/<int:task_id>/delete", methods=["POST"])
@login_required
def task_delete(task_id):
    """Delete a task."""
    conn = get_connection()
    try:
        cur = conn.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        if not cur.fetchone():
            flash("Task not found.", "error")
            return redirect(url_for("index"))
        conn.execute("DELETE FROM taskslog WHERE task_id = ?", (task_id,))
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        flash("Task deleted.", "success")
    finally:
        conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
