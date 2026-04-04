from fastapi import APIRouter, Depends

from api.deps import get_current_user
from db.models import User
from schemas.todo import TodoCreate, TodoRead, TodoUpdate, TodoPatch
from services.todo_service import (create_todo, get_todo_by_id, get_todos_user,
                                   ensure_todo_owner, update_todo_by_id, patch_todo_by_id,
                                   delete_todo)
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
    todo = await get_todo_by_id(db, todo_id)
    ensure_todo_owner(todo, current_user)
    return todo


@todo_router.get('/todos', response_model=list[TodoRead])
async def get_todos_endpoint(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await get_todos_user(session=db, user_id=current_user.id)


@todo_router.put('/todos/{todo_id}', response_model=TodoRead)
async def update_todo_endpoint(
        todo_id: int,
        todo_data: TodoUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await update_todo_by_id(db, todo_id, current_user, todo_data)


@todo_router.patch('/todos/{todo_id}', response_model=TodoRead)
async def patch_todo_endpoint(
        todo_id: int,
        todo_data: TodoPatch,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await patch_todo_by_id(db, todo_id, current_user, todo_data)

@todo_router.delete('/todos/{todo_id}')
async def delete_todo_endpoint(
        todo_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    await delete_todo(db, todo_id, current_user)
    return {"message": "Todo was deleted"}