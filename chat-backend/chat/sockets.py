import socketio
from auth.jwt import decode_token
from moderation.pipeline import moderate_message
from .manager import manager

sio = socketio.AsyncServer(cors_allowed_origins= "*")

@sio.event
async def connect(sid, environ, auth):
    try:
        token = auth["token"]
        payload = decode_token(token)
        user = payload["sub"]

        await manager.connect(sid, user)
        print("Connected:", user)
    
    except:
        return False #reject connection
    

@sio.event
async def chat_message(sid, data):
    user = manager.active.get(sid)

    message_data = {
        "user": user,
        "message": data["message"]
    }

    result = await moderate_message(message_data)

    # If blocked, only notify sender
    if result["status"] == "blocked":
        await sio.emit("moderation_notice", {
            "message": "‼️ Your message was bloked due to toxic content",
            "toxic": result["toxicity"]
        }, to=sid)
        return

    # Send to everyone
    await sio.emit("new_message", result)

@sio.event
async def disconnect(sid):
    await manager.disconnect(sid)