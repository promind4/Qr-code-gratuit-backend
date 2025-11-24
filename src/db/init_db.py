"""
Initialize the database by creating all tables
"""
from src.db.database import engine, Base
from src.db.models import User

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_db()
