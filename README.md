# Hangarin — Task & To‑Do Manager (Django)

Hangarin is a simple Django web application that helps users organize daily tasks, manage priorities and categories, add notes, and break down large tasks into smaller subtasks.

This project is built based on the provided ERD and midterm/final requirements:
- Virtual environment setup
- Version control (Git + GitHub)
- Deployment to PythonAnywhere
- Models with BaseModel timestamps, `__str__`, and status choices
- Admin customization (list display, filters, search)
- Data population (manual + Faker seeding)

---

## ERD / Data Models

Entities:
- **Priority** (name)
- **Category** (name)
- **Task** (title, description, deadline, status, category, priority, created_at, updated_at)
- **Note** (task, content, created_at, updated_at)
- **SubTask** (parent_task, title, status, created_at, updated_at)

Relations:
- Category 1—* Task
- Priority 1—* Task
- Task 1—* Note
- Task 1—* SubTask

---

## Tech Stack
- Python 3.x
- Django
- Faker (for generating fake data)
- SQLite (default in development)

---

## Setup Instructions (Local)

### 1) Clone the repository
```bash
git clone https://github.com/oaappp/Hangarin-Task-To-Do-Manager.git

cd hangarin
```

### 2) Create and activate virtual environment
Windows (PowerShell):
```bash
python -m venv myenv
myenv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5) Create admin user
```bash
python manage.py createsuperuser
```

### 6) Start the server
```bash
python manage.py runserver
```

Open:
- Admin: http://127.0.0.1:8000/admin/

---

## Populate Required Data

### A) Manual records (REQUIRED)

In Django Admin, add the following:

### Priority

- high
- medium
- low
- critical
- optional

### Category

- Work
- School
- Personal
- Finance
- Projects

### B) Generate fake data using Faker (REQUIRED)

This project includes a seeder command:

```bash
python manage.py seed
```

Optional arguments:

```bash
python manage.py seed --tasks 30 --notes 90 --subtasks 120
```