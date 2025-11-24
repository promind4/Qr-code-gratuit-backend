import shutil
import uuid
from pathlib import Path
from typing import Dict

from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from src.core.config import settings

router = APIRouter(prefix="/api/v1/upload", tags=["upload"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/")
async def upload_file(request: Request, file: UploadFile = File(...)) -> Dict[str, str]:
    try:
        # Validation
        MAX_FILE_SIZE = 2 * 1024 * 1024 # 2MB
        ALLOWED_TYPES = ["image/jpeg", "image/png", "image/svg+xml", "application/pdf"]
        
        if file.content_type not in ALLOWED_TYPES:
             raise HTTPException(status_code=400, detail="Type de fichier non supporté (JPG, PNG, SVG, PDF uniquement)")

        # Generate unique filename
        file_extension = Path(file.filename).suffix if file.filename else ""
        filename = f"{uuid.uuid4()}{file_extension}"
        file_path = UPLOAD_DIR / filename

        # Save file and check size
        size = 0
        try:
            with file_path.open("wb") as buffer:
                while True:
                    chunk = await file.read(1024 * 1024) # Read 1MB chunks
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > MAX_FILE_SIZE:
                        raise ValueError("File too large")
                    buffer.write(chunk)
        except ValueError:
            file_path.unlink(missing_ok=True)
            raise HTTPException(status_code=413, detail="Fichier trop volumineux (Max 2MB)")

        # Construct URL
        base_url = str(request.base_url).rstrip("/")
        file_url = f"{base_url}/uploads/{filename}"

        return {"url": file_url, "filename": filename}
    except HTTPException:
        raise
    except Exception as e:
        # Clean up if something else went wrong
        if 'file_path' in locals() and file_path.exists():
             try:
                 file_path.unlink()
             except:
                 pass
        raise HTTPException(status_code=500, detail=str(e))
