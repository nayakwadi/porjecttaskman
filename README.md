# Task Manager POC

A proof-of-concept task management application using **Flask** (latest) with **SQLite** and raw SQL. Includes simple user authentication, task creation/editing/deletion, assignment, and filtering.

## Features

- **User Authentication**: Register, login, logout (session-based, plain-text passwords)
- **Task Management**: Create, edit, delete tasks
- **Assignment**: Assign tasks to users
- **Statuses**: draft, refined, active, in-progress, completed, rejected
- **Filtering**: By status or by assigned user
- **Audit Trail**: `taskslog` table records task changes

## Requirements

- Python 3.13 or later
- Flask 3.x

## Setup and Run

### 1. Create and activate a virtual environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
# venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Flask app and run

```bash
export FLASK_APP=app
flask run
```

Or run directly:

```bash
python -m flask run
```

### 4. Access the app

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

- **Register** a new user
- **Login** with username/password
- Create tasks, assign to users, set status
- Filter tasks by status or assigned user

## Database

SQLite database file: `taskman.db` (created automatically in the project root).

**Tables:**

| Table    | Description                              |
|----------|------------------------------------------|
| users    | id, username, password, created_at       |
| tasks    | id, title, description, status, assigned_to, created_by, timestamps |
| taskslog | id, task_id, action, changed_by, changed_at, old_value, new_value   |

All database access uses raw SQL via the `sqlite3` module (no ORM).

## Security Note (POC Only)

- Passwords are stored in **plain text**
- No MFA or RBAC
- Not intended for production use

## ER DB Model Diagram

The database schema is documented in `db-model.mmd` (Mermaid ER diagram).

### How to View the Diagram

- **GitHub/GitLab** – Put the script in a `.md` file and they will render it
- **Mermaid Live Editor** – [mermaid.live](https://mermaid.live) – paste the script and export as PNG/SVG
- **VS Code / Cursor** – Use the Mermaid extension and preview the file
- **Notion, Confluence, etc.** – Use their Mermaid/code-block support to render it

### Legend

| Symbol | Meaning |
|--------|---------|
| PK | Primary key |
| UK | Unique constraint |
| FK | Foreign key |
| <code>&#124;&#124;--o{</code> | One-to-many relationship |