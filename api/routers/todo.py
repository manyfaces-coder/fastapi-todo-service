from fastapi import APIRouter, Depends

from api.deps import get_current_user
from db.models import User
from schemas.todo import TodoCreate, TodoRead, TodoUpdate
from services.todo_service import create_todo, get_todo_by_id, get_todos_user
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db

todo_router = APIRouter(tags=['Todos'])


@todo_router.post("/todos", response_model=TodoRead)
async def create_todo_endpoint(
        todo_data: TodoCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await create_todo(db, current_user.id, todo_data)


@todo_router.get('/todos/{todo_id}', response_model=TodoRead)
async def get_todo_by_id_endpoint(
        todo_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await get_todo_by_id(session=db, todo_id=todo_id, current_user=current_user)


@todo_router.get('/todos', response_model=list[TodoRead])
async def get_todos_endpoint(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await get_todos_user(session=db, user_id=current_user.id)
