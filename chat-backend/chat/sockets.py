import socketio
from auth.jwt import decode_token
from moderation.pipeline import moderate_message

from redis_client import redis_client
from db import SessionLocal
from models.message import Message


# 🔥 Redis-backed Socket.IO server (scalable, multi-instance safe)
sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    async_mode="asgi",
    client_manager=socketio.AsyncRedisManager("redis://localhost:6379")
)

# Local in-memory mapping (per worker only)
connected_users = {}   # sid -> username


# ---------------------------------------------------
# 🔐 CONNECT — Authenticate user & mark online
# ---------------------------------------------------
@sio.event
async def connect(sid, environ, auth):
    try:
        token = auth.get("token")
        payload = decode_token(token)
        user = payload["sub"]

        # Save sid -> user mapping
        connected_users[sid] = user

        # Mark user online in Redis
        await redis_client.sadd("online_users", user)

        # Broadcast updated online users list
        users = await redis_client.smembers("online_users")
        users = [u.decode() if isinstance(u, bytes) else u for u in users]

        await sio.emit("online_users", users)

        print(f"🟢 Connected: {user}")

    except Exception as e:
        print("❌ Connection rejected:", e)
        return False   # Reject socket connection


# ---------------------------------------------------
# 👥 JOIN ANY ROOM (PUBLIC / GROUP / PRIVATE)
# ---------------------------------------------------
@sio.event
async def join_room(sid, data):
    """
    data = {
        room: "global" | "chat_12" | "private_user1_user2"
    }
    """
    room = data["room"]
    user = connected_users.get(sid)

    await sio.enter_room(sid, room)

    print(f"👥 {user} joined room {room}")

    await sio.emit("system", {
        "message": f"{user} joined the room"
    }, room=room)


# ---------------------------------------------------
# 👋 LEAVE ROOM
# ---------------------------------------------------
@sio.event
async def leave_room(sid, data):
    room = data["room"]
    user = connected_users.get(sid)

    await sio.leave_room(sid, room)

    print(f"👋 {user} left room {room}")

    await sio.emit("system", {
        "message": f"{user} left the room"
    }, room=room)


# ---------------------------------------------------
# 🔐 PRIVATE ROOM CREATION (1-to-1 CHAT)
# ---------------------------------------------------
def private_room(user1: str, user2: str):
    users = sorted([user1, user2])
    return f"private_{users[0]}_{users[1]}"


@sio.event
async def start_private_chat(sid, data):
    """
    data = { target_user: "friend@gmail.com" }
    """
    user = connected_users.get(sid)
    target = data["target_user"]

    room = private_room(user, target)

    # Join creator to private room
    await sio.enter_room(sid, room)

    # Notify sender with room id
    await sio.emit("private_room_created", {
        "room": room,
        "with": target
    }, to=sid)

    print(f"🔐 Private room created: {room}")


# ---------------------------------------------------
# ✍️ TYPING INDICATOR (ROOM SCOPED)
# ---------------------------------------------------
@sio.event
async def typing(sid, data):
    """
    data = { room: "room_id" }
    """
    user = connected_users.get(sid)

    await sio.emit("typing", {
        "user": user
    }, room=data["room"], skip_sid=sid)


# ---------------------------------------------------
# 💬 CHAT MESSAGE — ML MODERATION + DB + ROOMS
# ---------------------------------------------------
@sio.event
async def chat_message(sid, data):
    """
    data = {
        room: "global" | "chat_1" | "private_x_y",
        message: "hello",
        chat_id: 1,
        user_id: 5
    }
    """

    user = connected_users.get(sid)

    if not user:
        return

    # 🔹 Call ML moderation pipeline
    result = await moderate_message({
        "user": user,
        "message": data["message"]
    })

    # 🔹 If BLOCKED → notify only sender
    if result["status"] == "blocked":
        await sio.emit("moderation_notice", {
            "message": "‼️ Your message was blocked due to toxic content",
            "toxicity": result["toxicity"]
        }, to=sid)

        # Update live toxicity meter for sender
        await sio.emit("toxicity_update", {
            "toxicity": result["toxicity"]
        }, to=sid)

        return

    # 🔹 Save approved / censored message to PostgreSQL
    async with SessionLocal() as db:
        msg = Message(
            chat_id=data["chat_id"],
            user_id=data["user_id"],
            content=result["message"],
            toxicity=result["toxicity"],
            status=result["status"]
        )
        db.add(msg)
        await db.commit()

    # 🔹 Update sender toxicity meter
    await sio.emit("toxicity_update", {
        "toxicity": result["toxicity"]
    }, to=sid)

    # 🔹 Broadcast message to room (Redis-backed, scalable)
    await sio.emit("new_message", result, room=data["room"])


# ---------------------------------------------------
# 🔴 DISCONNECT — Remove from online users
# ---------------------------------------------------
@sio.event
async def disconnect(sid):
    user = connected_users.get(sid)

    if user:
        # Remove from Redis online set
        await redis_client.srem("online_users", user)

        # Remove local mapping
        connected_users.pop(sid, None)

        # Broadcast updated online users
        users = await redis_client.smembers("online_users")
        users = [u.decode() if isinstance(u, bytes) else u for u in users]

        await sio.emit("online_users", users)

        print(f"🔴 Disconnected: {user}")
