# db.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# use the same user you used with psql (prasoon)
DATABASE_URL = os.getenv(
"DATABASE_URL",
"postgresql+asyncpg://prasoon:prasoon@localhost:5432/chatdb")

engine = create_async_engine(DATABASE_URL, echo=True)

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



# DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/chatdb"
