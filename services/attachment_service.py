import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.attachment import AttachmentUploadRequest, AttachmentUploadResponse
from db.models.attachment import Attachment
from db.models.user import User
from .todo_service import get_todo_by_id, ensure_todo_owner
from core.config import MAX_ATTACHMENT_SIZE, ALLOWED_MIME_TYPES


async def request_attachment_upload(
        session: AsyncSession,
        todo_id: int,
        current_user: User,
        attachment_data: AttachmentUploadRequest,
) -> AttachmentUploadResponse:
    todo = await get_todo_by_id(session, todo_id)

    ensure_todo_owner(todo, current_user)

    if attachment_data.size > MAX_ATTACHMENT_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

    if attachment_data.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    storage_key = f"attachments/{todo_id}/{uuid.uuid4()}_{attachment_data.filename}"
    upload_url = f"uploads/{storage_key}"

    attachment = Attachment(
        todo_id=todo_id,
        filename=attachment_data.filename,
        size=attachment_data.size,
        content_type=attachment_data.content_type,
        storage_key=storage_key,
    )

    session.add(attachment)
    await session.commit()
    await session.refresh(attachment)

    return AttachmentUploadResponse(
        upload_url=upload_url,
        storage_key=storage_key,
    )
