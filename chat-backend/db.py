# db.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://prasoon:prasoon@localhost:5432/chatdb"
)

# 🔥 AUTO-DETECT WHETHER SSL IS NEEDED
connect_args = {}

# Neon / cloud postgres requires SSL
if "neon.tech" in DATABASE_URL or "render.com" in DATABASE_URL:
    connect_args = {"ssl": True}

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 🔥 SINGLE GLOBAL BASE (VERY IMPORTANT)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
