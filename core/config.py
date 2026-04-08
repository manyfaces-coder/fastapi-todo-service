import os
from dotenv import load_dotenv

load_dotenv()

JWT_KEY = os.getenv("JWT_KEY")
if not JWT_KEY:
    raise RuntimeError("JWT_KEY is not set")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# отдельная ссылка на БД для Alembic, т.к. в текущей конфигурации он работает синхронно
ALEMBIC_DATABASE_URL = os.getenv("ALEMBIC_DATABASE_URL")
if not ALEMBIC_DATABASE_URL:
    raise RuntimeError("ALEMBIC_DATABASE_URL is not set")


MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "application/pdf",
    "text/plain",
}