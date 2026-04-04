from pydantic import BaseModel, Field
from datetime import datetime

class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    # остальные поля на сервере


class TodoRead(BaseModel):
    id: int
    owner_id: int
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
    version: int


class TodoUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    completed: bool
    version: int


class TodoPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None
    version: int
