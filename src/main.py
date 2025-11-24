from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from fastapi.staticfiles import StaticFiles
from src.api.endpoints.auth import router as auth_router
from src.api.endpoints.qrcode import router as qrcode_router
from src.api.endpoints.upload import router as upload_router
from src.core.config import settings
from src.core.rate_limiter import limiter


app = FastAPI(
    title="QR Code Generation API",
    version="1.0.0",
    description="Stateless API générant des QR codes de différentes formes et formats.",
)

# Configuration du rate limiting
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Fix pour erreur 400 sur Render : On accepte tous les noms de domaine
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    # Autorise toutes les origines (plus simple et robuste car pas de cookies)
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth_router)
app.include_router(qrcode_router)
app.include_router(upload_router)


@app.get("/health", tags=["health"])
def health_check() -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={"status": "ok", "environment": settings.environment},
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Trop de requêtes envoyées ; veuillez réessayer plus tard.",
            "error_code": "RATE001",
        },
    )


@app.on_event("startup")
async def startup_event():
    """Initialize database and clean up old uploads on startup"""
    from src.db.init_db import init_db
    import time
    from pathlib import Path
    
    try:
        init_db()
    except Exception as e:
        print(f"Database initialization: {e}")
        
    # Cleanup old uploads (> 24h)
    try:
        upload_dir = Path("uploads")
        if upload_dir.exists():
            now = time.time()
            cutoff = now - (24 * 3600) # 24 hours
            count = 0
            for f in upload_dir.iterdir():
                if f.is_file() and f.stat().st_mtime < cutoff:
                    try:
                        f.unlink()
                        count += 1
                    except Exception as e:
                        print(f"Error deleting {f}: {e}")
            if count > 0:
                print(f"Cleaned up {count} old upload files")
    except Exception as e:
        print(f"Cleanup error: {e}")
