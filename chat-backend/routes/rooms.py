from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth.jwt import decode_token
from db import get_db
from models.room import Room
from models.room_member import RoomMember

router = APIRouter()

# create new room
@router.post("/create")
async def create_room(data: dict, db: AsyncSession = Depends(get_db)):
    name = data["name"]
    user_id = data["user_id"]

    room = Room(
        name=name,
        is_private = False,
        created_by= user_id
    )

    db.add(room)
    await db.commit()
    await db.refresh(room)

    # Add creator as a memer
    member = RoomMember(room_id= room.id, user_id=user_id)
    db.add(member)
    await db.commit()

    return {"room_id":room.id, "name":room.name}

# List rooms for user
@router.get("/my/{user_id}")
async def my_rooms(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Room)
        .join(RoomMember)
        .where(RoomMember.user_id == user_id)
    )

    rooms = result.scalars().all()

    return [{"id": r.id, "name": r.name} for r in rooms]