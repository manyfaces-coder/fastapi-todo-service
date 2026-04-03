from db.models.todo import Todo
from fastapi import HTTPException, Depends
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.todo import TodoCreate
from db.models.user import User


async def get_todo_by_id(session: AsyncSession, todo_id:int, current_user: User) -> Todo|None:
    query = select(Todo).where(Todo.id == todo_id)
    result = await session.execute(query)
    todo = result.scalar_one_or_none()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return todo


async def get_todos_user(session: AsyncSession, user_id:int) -> list[Todo]:
    query = select(Todo).where(Todo.owner_id==user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def create_todo(session: AsyncSession, owner_id:int, todo_data: TodoCreate) -> Todo:
    todo_dict = todo_data.model_dump()
    todo = Todo(**todo_dict, owner_id=owner_id)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    return todo


async def update_todo_by_id(session: AsyncSession, todo_data) -> Todo:
    pass


async def patch_todo_by_id(session: AsyncSession, todo_data) -> Todo:
    pass


async def delete_todo(session: AsyncSession, todo_id:int):
    pass