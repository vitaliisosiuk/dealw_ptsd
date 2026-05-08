# Deal with PTSD

Web platform for PTSD support with self-help tools, assessments, trigger mapping, inspirational cards, meditation, and a personal journal.

## Tech Stack

- Python 3.12
- Django 6
- SQLite (development/local use)
- Tailwind CSS (via `django-tailwind`)
- Docker & Docker Compose

## Features

- User authentication and profile
- PTSD assessments (multiple tests with stored results)
- Trigger mapping and trigger summaries
- Inspirational cards with image export
- Meditation player (duration-based options)
- Personal journal with writing prompts

## Project Structure

- `accounts/` - authentication, profile, account details
- `assessments/` - tests, scoring logic, result pages
- `tools/` - support tools (triggers, cards, meditation, journal, art)
- `core/` - landing and informational pages
- `config/` - Django settings, URLs, WSGI/ASGI

## Local Setup (without Docker)

1. Create and activate a virtual environment:
   - Linux/macOS:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. (Optional) Seed inspirational quotes:
   ```bash
   python manage.py seed_inspirational_quotes --clear
   ```
5. Start development server:
   ```bash
   python manage.py runserver
   ```

App URL: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Docker Setup

### Prerequisites

- Docker
- Docker Compose (v2+)

### Run

```bash
docker compose up --build
```

The container automatically runs migrations on startup.

App URL: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Stop

```bash
docker compose down
```

### Rebuild from scratch

```bash
docker compose down
docker compose up --build
```

## Useful Management Commands

- Apply migrations:
  ```bash
  python manage.py migrate
  ```
- Create admin user:
  ```bash
  python manage.py createsuperuser
  ```
- Seed trigger options:
  ```bash
  python manage.py seed_triggers
  ```
- Seed inspirational quotes:
  ```bash
  python manage.py seed_inspirational_quotes --clear
  ```

## Notes

- This project currently uses SQLite and is intended for development/academic demonstration.
- For production deployment, switch to PostgreSQL (or another production-grade DB), configure static/media serving, and secure environment variables.

