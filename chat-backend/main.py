from fastapi import FastAPI
import socketio
from chat.sockets import sio
from auth.routes import router as auth_router

app = FastAPI()

# REST auth routes
app.include_router(auth_router, prefix="/auth")

# Mount websocket app
app.mount("/ws", socketio.ASGIApp(sio))

@app.get("/")
async def root():
    return {"status": "chat backend running"}