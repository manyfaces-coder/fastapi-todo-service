from db.models.todo import Todo
from fastapi import HTTPException, Depends
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.todo import TodoCreate, TodoUpdate, TodoPatch
from db.models.user import User


async def get_todo_by_id(session: AsyncSession, todo_id: int) -> Todo | None:
    query = select(Todo).where(Todo.id == todo_id)
    result = await session.execute(query)
    todo = result.scalar_one_or_none()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


def ensure_todo_owner(todo: Todo, current_user: User) -> None:
    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")


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


async def update_todo_by_id(
        session: AsyncSession,
        todo_id: int,
        current_user: User,
        todo_data: TodoUpdate,
) -> Todo:
    todo = await get_todo_by_id(session, todo_id)

    ensure_todo_owner(todo, current_user)

    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.completed = todo_data.completed
    todo.updated_at = datetime.utcnow()

    if todo.completed:
        todo.completed_at = datetime.utcnow()

    else:
        todo.completed_at = None

    if todo.version != todo_data.version:
        raise HTTPException(status_code=409, detail="Version conflict")

    todo.version += 1

    await session.commit()
    await session.refresh(todo)
    return todo


async def patch_todo_by_id(
        session: AsyncSession,
        todo_id: int,
        current_user: User,
        todo_data: TodoPatch
) -> Todo:
    todo = await get_todo_by_id(session, todo_id)

    ensure_todo_owner(todo, current_user)
    if todo.version != todo_data.version:
        raise HTTPException(status_code=409, detail="Version conflict")
    # поля, которые не были явно заданы при создании экземпляра модели, будут исключены из возвращаемого словаря
    update_data = todo_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(todo, field, value)

    todo.updated_at = datetime.utcnow()

    if "completed" in update_data:
        if todo.completed:
            todo.completed_at = datetime.utcnow()
        else:
            todo.completed_at = None

    todo.version += 1

    await session.commit()
    await session.refresh(todo)

    return todo


async def delete_todo(session: AsyncSession, todo_id:int, current_user) -> None:
    todo = await get_todo_by_id(session, todo_id)
    ensure_todo_owner(todo, current_user)

    await session.delete(todo)
    await session.commit()