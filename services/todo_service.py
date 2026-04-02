from db.models.todo import Todo
from fastapi import HTTPException, Depends
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.todo import TodoCreate


async def get_todo_by_id(session: AsyncSession, todo_id:int) -> Todo|None:
    query = select(Todo).where(Todo.id == todo_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_todos_user(session: AsyncSession, user_id:int) -> list[Todo]:
    query = select(Todo).where(Todo.owner_id==user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def create_todo(session: AsyncSession, owner_id:int, todo_data: TodoCreate) -> Todo:
    todo_dict = todo_data.model_dump(todo_data)
    todo = Todo(**todo_dict, owner_id=owner_id)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    return todo

