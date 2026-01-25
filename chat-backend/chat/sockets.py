import os
import socketio
from auth.jwt import decode_token
from moderation.pipeline import moderate_message

from redis_client import redis_client
from db import SessionLocal
from models.message import Message
from sqlalchemy.future import select
from models.room_member import RoomMember
from models.room import Room


# 🔥 Redis-backed Socket.IO server (scalable)
sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    async_mode="asgi",
    client_manager=socketio.AsyncRedisManager(os.getenv("REDIS_URL"),"redis://localhost:6379")
)

# Local sid -> user mapping
connected_users = {}   # sid -> {"email": str, "user_id": int}


# ---------------------------------------------------
# 🔐 CONNECT — Authenticate user & auto join rooms
# ---------------------------------------------------
@sio.event
async def connect(sid, environ, auth):
    try:
        token = auth.get("token")
        payload = decode_token(token)

        user_email = payload["sub"]
        user_id = payload["user_id"]

        # Save mapping
        connected_users[sid] = {
            "email": user_email,
            "user_id": user_id
        }

        # Mark user online
        await redis_client.sadd("online_users", user_email)

        users = await redis_client.smembers("online_users")
        users = [u.decode() if isinstance(u, bytes) else u for u in users]

        await sio.emit("online_users", users)

        # 🔥 Auto join all persistent rooms from DB
        async with SessionLocal() as db:
            result = await db.execute(
                select(Room)
                .join(RoomMember)
                .where(RoomMember.user_id == user_id)
            )

            rooms = result.scalars().all()

            for room in rooms:
                await sio.enter_room(sid, f"room_{room.id}")
                print(f"👥 {user_email} auto-joined room_{room.id}")

        # Always join global
        await sio.enter_room(sid, "global")

        print(f"🟢 Connected: {user_email}")

    except Exception as e:
        print("❌ Connection rejected:", e)
        return False


# ---------------------------------------------------
# 👥 JOIN ROOM
# ---------------------------------------------------
@sio.event
async def join_room(sid, data):
    room = data["room"]
    user = connected_users.get(sid)

    await sio.enter_room(sid, room)

    await sio.emit("system", {
        "message": f"{user['email']} joined the room"
    }, room=room)


# ---------------------------------------------------
# 👋 LEAVE ROOM
# ---------------------------------------------------
@sio.event
async def leave_room(sid, data):
    room = data["room"]
    user = connected_users.get(sid)

    await sio.leave_room(sid, room)

    await sio.emit("system", {
        "message": f"{user['email']} left the room"
    }, room=room)


# ---------------------------------------------------
# 🔐 PRIVATE ROOM CREATION
# ---------------------------------------------------
def private_room(user1: str, user2: str):
    users = sorted([user1, user2])
    return f"private_{users[0]}_{users[1]}"


@sio.event
async def start_private_chat(sid, data):
    user = connected_users.get(sid)
    target = data["target_user"]

    room = private_room(user["email"], target)

    await sio.enter_room(sid, room)

    await sio.emit("private_room_created", {
        "room": room,
        "with": target
    }, to=sid)

    print(f"🔐 Private room created: {room}")


# ---------------------------------------------------
# ✍️ TYPING INDICATOR
# ---------------------------------------------------
@sio.event
async def typing(sid, data):
    user = connected_users.get(sid)

    await sio.emit("typing", {
        "user": user["email"]
    }, room=data["room"], skip_sid=sid)


# ---------------------------------------------------
# 💬 CHAT MESSAGE — ML + DB + ROOMS
# ---------------------------------------------------
@sio.event
async def chat_message(sid, data):
    """
    data = {
        room: "global" | "room_1" | "private_x_y",
        message: "hello",
        chat_id: 1
    }
    """

    user = connected_users.get(sid)

    if not user:
        return

    # 🔹 Run ML moderation
    result = await moderate_message({
        "user": user["email"],
        "message": data["message"]
    })

    # 🔹 If BLOCKED
    if result["status"] == "blocked":
        await sio.emit("moderation_notice", {
            "message": "‼️ Your message was blocked due to toxic content",
            "toxicity": result["toxicity"]
        }, to=sid)

        await sio.emit("toxicity_update", {
            "toxicity": result["toxicity"]
        }, to=sid)

        return

    # 🔹 Save message
    async with SessionLocal() as db:
        msg = Message(
            chat_id=data.get("chat_id", 1),
            user_id=user["user_id"],
            content=result["message"],
            toxicity=result["toxicity"],
            status=result["status"]
        )
        db.add(msg)
        await db.commit()

    # 🔹 Update toxicity meter
    await sio.emit("toxicity_update", {
        "toxicity": result["toxicity"]
    }, to=sid)

    # 🔹 Broadcast to room
    await sio.emit("new_message", {
        "user": user["email"],
        "message": result["message"],
        "toxicity": result["toxicity"],
        "status": result["status"],
        "moderated_text": result["moderated_text"]
    }, room=data["room"])


# ---------------------------------------------------
# 🔴 DISCONNECT
# ---------------------------------------------------
@sio.event
async def disconnect(sid):
    user = connected_users.get(sid)

    if user:
        await redis_client.srem("online_users", user["email"])
        connected_users.pop(sid, None)

        users = await redis_client.smembers("online_users")
        users = [u.decode() if isinstance(u, bytes) else u for u in users]

        await sio.emit("online_users", users)

        print(f"🔴 Disconnected: {user['email']}")
