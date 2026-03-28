import jwt
import secrets
from fastapi import HTTPException, Depends
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from core.config import JWT_KEY
from schemas.user import UserCreate
from schemas.auth import Token
from db.models.user import User
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
DUMMY_HASH = pwd_context.hash("dummy_password")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def create_jwt_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=100)
    data.update({"exp": expire})
    return jwt.encode(data, JWT_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=404, detail="Token is missing")
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token", headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def register_user(session: AsyncSession, username: str, password: str) -> User:
    user_from_db = await get_user_by_username(session, username)
    if user_from_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed_password, role="user")

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user



async def authenticate_user(session: AsyncSession, username: str, password: str) -> User:
    user_from_db = await get_user_by_username(session, username)

    username_ok = (user_from_db is not None and
                   secrets.compare_digest(user_from_db.username.encode("utf-8"), username.encode("utf-8")))

    hashed_password = user_from_db.hashed_password if user_from_db is not None else DUMMY_HASH
    password_ok = pwd_context.verify(password, hashed_password)

    if username_ok and password_ok:
        return user_from_db

    raise HTTPException(status_code=401, detail="Invalid username or password")



