
import asyncio
from db import engine, Base

# 🔥 import ALL models so they register with Base
from models.user import User
from models.chats import Chat
from models.message import Message


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init())
