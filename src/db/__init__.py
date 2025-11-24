# Import all models here so Alembic can detect them
from src.db.database import Base
from src.db.models import User

__all__ = ["Base", "User"]
