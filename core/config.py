import os
from dotenv import load_dotenv

load_dotenv()

JWT_KEY = os.getenv("JWT_KEY")
if not JWT_KEY:
    raise RuntimeError("JWT_KEY is not set")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")