"""Database module - raw SQL with sqlite3 (no ORM)."""

import sqlite3
from pathlib import Path

# Database file path
DB_PATH = Path(__file__).parent / "taskman.db"

# Valid task statuses
TASK_STATUSES = ("draft", "refined", "active", "in-progress", "completed", "rejected")


def get_connection():
    """Return a database connection."""
    return sqlite3.connect(DB_PATH)


def get_connection_with_row_factory():
    """Return a connection that returns rows as dict-like objects."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they do not exist."""
    conn = get_connection()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'draft',
                assigned_to INTEGER,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assigned_to) REFERENCES users(id),
                FOREIGN KEY (created_by) REFERENCES users(id),
                CHECK (status IN ('draft', 'refined', 'active', 'in-progress', 'completed', 'rejected'))
            );

            CREATE TABLE IF NOT EXISTS taskslog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                changed_by INTEGER NOT NULL,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                old_value TEXT,
                new_value TEXT,
                FOREIGN KEY (task_id) REFERENCES tasks(id),
                FOREIGN KEY (changed_by) REFERENCES users(id)
            );

            CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
            CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to);
        """)
        conn.commit()
    finally:
        conn.close()
