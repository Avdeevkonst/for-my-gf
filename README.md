# Telegram Bot with Content Management

This is a Telegram bot that allows users to manage content with steps and messages.

## Features

- User registration and management
- Content management with steps (1-20)
- Content listing
- Database storage with PostgreSQL

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
```

2. Install dependencies:
```bash
uv pip install -r requirements.txt
```

3. Create a PostgreSQL database:
```bash
createdb telegram_bot
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your configuration

5. Initialize the database:
```bash
alembic upgrade head
```

6. Run the bot:
```bash
python -m src.bot.bot
```

## Usage

The bot supports the following commands:

- `/start` - Start the bot and register user
- `/add_content` - Add new content with step and message
- `/list_content` - List all your content

When adding content, use the following format:
```
Шаг: [номер от 1 до 20]
Контент: [ваш контент]
Сообщение: [ваше сообщение]
```

## Project Structure

```
src/
├── bot/
│   ├── handlers/
│   │   ├── commands.py
│   │   └── content.py
│   ├── middlewares/
│   │   └── db.py
│   └── bot.py
└── database/
    ├── models.py
    └── config.py
```
