from pydantic import BaseModel, Field
from datetime import datetime


class AttachmentRead(BaseModel):
    id: int
    todo_id: int
    filename: str
    size: int
    content_type: str
    storage_key: str
    created_at: datetime


class AttachmentUploadRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    size: int = Field(gt=0)
    content_type: str = Field(min_length=1, max_length=100)


class AttachmentUploadResponse(BaseModel):
    upload_url: str
    storage_key: str
