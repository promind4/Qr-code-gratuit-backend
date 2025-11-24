from enum import Enum
from typing import Optional, Set
from pydantic import BaseModel, Field, validator


class QRCodeFormat(str, Enum):
    png = "png"
    jpeg = "jpeg"
    svg = "svg"
    pdf = "pdf"


class QRCodeRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    format: QRCodeFormat = QRCodeFormat.png
    size: int = Field(300, ge=100, le=1000)
    color: str = Field("#000000", pattern=r"^#([A-Fa-f0-9]{6})$")
    background: str = Field("#FFFFFF", pattern=r"^#([A-Fa-f0-9]{6})$")
    margin: int = Field(4, ge=0, le=50)
    error_correction: str = Field("M")
    logo_url: Optional[str] = None
    body_style: str = Field("square")  # square, circle, rounded, gapped, vertical, horizontal
    eye_style: str = Field("square")   # square, circle, rounded
    sticker_type: Optional[str] = None  # grid, bubble, film, book, beer

    @validator("error_correction")
    def check_error_correction(cls, value: str) -> str:
        allowed: Set[str] = {"L", "M", "Q", "H"}
        if value not in allowed:
            raise ValueError("Erreur inconnue (L, M, Q, H attendus)")
        return value


class QRCodeResponse(BaseModel):
    request_id: str
    format: QRCodeFormat
    size: int
