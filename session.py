from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from typing import Generator

# Database URL - can be configured via environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./ai_interview_platform.db"  # Default to SQLite for development
)

# For PostgreSQL in production, use:
# DATABASE_URL = "postgresql://username:password@localhost/ai_interview_platform"

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},  # Only needed for SQLite
        echo=False  # Set to True for SQL query logging
    )
else:
    engine = create_engine(DATABASE_URL, echo=False)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def get_db() -> Generator:
    """
    Dependency to get database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all tables in the database.
    """
    from app.models.database import Base
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """
    Drop all tables in the database.
    """
    from app.models.database import Base
    Base.metadata.drop_all(bind=engine)

