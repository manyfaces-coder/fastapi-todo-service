import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.attachment import AttachmentUploadRequest, AttachmentUploadResponse
from db.models.attachment import Attachment
from db.models.user import User
from .todo_service import get_todo_by_id, ensure_todo_owner
from core.config import MAX_ATTACHMENT_SIZE, ALLOWED_MIME_TYPES
from sqlalchemy import select


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


async def get_attachment_by_id(
        session: AsyncSession,
        attachment_id: int
) -> Attachment | None:
    query = select(Attachment).where(Attachment.id == attachment_id)
    result = await session.execute(query)
    attachment = result.scalar_one_or_none()

    if attachment is None:
        raise HTTPException(status_code=404, detail="File not found")

    return attachment


async def delete_attachment(
        session: AsyncSession,
        attachment_id: int,
        current_user: User,
):
    attachment = await get_attachment_by_id(session, attachment_id)

    todo = await get_todo_by_id(session, attachment.todo_id)

    ensure_todo_owner(todo, current_user)

    await session.delete(attachment)
    await session.commit()
