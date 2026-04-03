from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from db.models.user import User
from services.auth_service import oauth2_scheme, get_user_from_token, get_user_by_username


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    username = get_user_from_token(token)
    user = await get_user_by_username(db, username)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
