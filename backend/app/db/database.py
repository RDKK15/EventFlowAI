from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

# Import all model modules so every mapped class is registered with
# this Base before any relationship() is resolved, regardless of which
# single model a caller actually needed (see app/models/__init__.py for
# the full explanation). This runs once, here, because every code path
# that touches the database -- app.main, alembic/env.py, services,
# standalone scripts -- already imports from app.db.database.
from app import models  # noqa: F401,E402


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()