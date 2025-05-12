# Content Management System

A FastAPI-based content management system with admin interface, Telegram bot, and file storage support.

## Features

- FastAPI-based REST API
- Admin interface with SQLAdmin
- Telegram bot for content management
- Telegram ID-based authentication for admin panel
- File storage using MinIO
- PostgreSQL database (async)
- Modern dependency management with `uv`
- Docker support

## Requirements

For local development:
- Python 3.13+
- PostgreSQL
- MinIO server
- `uv` package manager
- Telegram Bot Token

For Docker:
- Docker
- Docker Compose

## Installation

### Local Development
1. Clone the repository
2. Install dependencies:
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Docker
1. Clone the repository
2. Create `.env` file (see Configuration section)
3. Run with docker-compose:
```bash
docker-compose up -d
```

## Configuration

Create `.env` file with the following variables:

```env
# PostgreSQL
PG_HOST=postgres
PG_PORT=5432
PG_NAME=dbname
PG_USER=postgres
PG_PASS=password

# MinIO
MINIO_ENDPOINT=play.min.io
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key
MINIO_PUBLIC_BUCKET=public
MINIO_SECURE=true  # Use HTTPS

# Admin Access
ADMIN_SECRET_KEY=your-secret-key

# Telegram Bot
BOT_TOKEN=your-bot-token  # Get from @BotFather

# API
API_PORT=8000  # Port to expose FastAPI

# Network (for docker-compose)
EXTERNAL_NETWORK=shared_network  # External network name where PostgreSQL and MinIO are running

# Debug
ECHO=false  # Set to true to enable SQL query logging
```

## Running

### Local Development
1. Start the application (this will start both FastAPI and Telegram bot):
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker
1. Start the application:
```bash
docker-compose up -d
```

2. View logs:
```bash
docker-compose logs -f
```

3. Stop the application:
```bash
docker-compose down
```

Access the admin interface at: http://localhost:8000/admin

## Telegram Bot

The bot provides the following commands:
- `/start` - Initialize user
- `/add_content` - Add new content with step number
- `/list_content` - List all your content

The bot runs in polling mode alongside the FastAPI application.

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
├── bot/
│   ├── bot.py       # Bot initialization
│   ├── handlers/    # Bot command handlers
│   ├── middlewares/ # Bot middlewares
│   └── utils/       # Bot utilities
├── config/
│   └── settings.py  # Application settings
├── database/
│   ├── models.py    # SQLAlchemy models
│   └── session.py   # Database connection
├── storage/
│   └── minio.py     # MinIO integration
└── main.py          # Application entry point
```
