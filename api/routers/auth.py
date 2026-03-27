from fastapi import APIRouter, Depends
from schemas.auth import Token
from services.auth_service import authenticate_user, create_jwt_token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
auth_router = APIRouter(tags=['Authentication'])


@auth_router.post("/login", response_model=Token)
async def login(user_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(session=db,
                             username=user_data.username,
                             password=user_data.password)
    jwt_token = create_jwt_token({'sub': user.username})
    return {'access_token': jwt_token, 'token_type': 'bearer'}
