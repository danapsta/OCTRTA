import os

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "SQLAlchemy is required for the persistence layer. Install it with 'pip install SQLAlchemy'."
    ) from exc

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./calendar_sync.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
