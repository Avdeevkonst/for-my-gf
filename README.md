# Content Management System

A FastAPI-based content management system with admin interface and file storage support.

## Features

- FastAPI-based REST API
- Admin interface with SQLAdmin
- Telegram ID-based authentication for admin panel
- File storage using MinIO
- PostgreSQL database (async)
- Modern dependency management with `uv`

## Requirements

- Python 3.13+
- PostgreSQL
- MinIO server
- `uv` package manager

## Installation

1. Clone the repository
2. Install dependencies:
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Configuration

Create `.env` file with the following variables:

```env
# PostgreSQL
POSTGRES_DSN=postgresql+asyncpg://user:password@localhost:5432/dbname

# MinIO
MINIO_ENDPOINT=play.min.io
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key
MINIO_BUCKET=your-bucket-name
MINIO_SECURE=true  # Use HTTPS

# Admin Access
ADMIN_TELEGRAM_IDS=[123456789, 987654321]  # List of allowed Telegram IDs
```

## Running

1. Start the application:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

2. Access the admin interface at: http://localhost:8000/admin

## Admin Interface

The admin interface provides CRUD operations for:
- Users (view/edit only, creation via Telegram bot)
- Content (full CRUD with file upload support)

Authentication is required using Telegram ID from the allowed list.

## Development

- Code style: flake8 with WPS plugin
- Linting: ruff
- Package management: uv

## Project Structure

```
src/
├── admin/
│   ├── auth.py      # Admin authentication
│   └── models.py    # Admin model views
├── config/
│   └── settings.py  # Application settings
├── database/
│   ├── models.py    # SQLAlchemy models
│   └── session.py   # Database connection
├── storage/
│   └── minio.py     # MinIO integration
└── main.py          # Application entry point
```
