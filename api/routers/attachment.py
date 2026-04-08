from fastapi import APIRouter, Depends

from api.deps import get_current_user
from db.models import User
from schemas.attachment import AttachmentUploadRequest, AttachmentUploadResponse
from services.attachment_service import request_attachment_upload
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db


attachment_router = APIRouter(tags=["Attachment"])


@attachment_router.post("/todos/{todo_id}/attachments/request-upload", response_model=AttachmentUploadResponse)
async def request_attachment_upload_endpoint(
        todo_id: int,
        attachment_data: AttachmentUploadRequest,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    return await request_attachment_upload(
        session=db,
        todo_id=todo_id,
        current_user=current_user,
        attachment_data=attachment_data,
    )
