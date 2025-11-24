from typing import Optional
from fastapi import APIRouter, Depends, Header, Response, status, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.core.rate_limiter import limiter
from src.core.security import get_current_user, get_optional_current_user
from src.schemas.qrcode import QRCodeRequest
from src.services.qrcode_service import generate_qr

router = APIRouter(prefix="/api/v1/qrcode", tags=["qrcode"])


@router.post("/generate")
async def generate_qrcode(
    payload: QRCodeRequest,
    current_user: Optional[dict] = Depends(get_optional_current_user),
    user_agent: str | None = Header(None),
):
    request_id, payload_bytes, content_type = generate_qr(payload)
    headers = {
        "X-QRCode-Request-ID": request_id,
        "X-QRCode-Size": str(len(payload_bytes)),
        "Content-Type": content_type,
    }
    return Response(content=payload_bytes, headers=headers, media_type=content_type)
