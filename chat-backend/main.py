from fastapi import FastAPI
import socketio
from chat.sockets import sio
from auth.routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST auth routes
app.include_router(auth_router, prefix="/auth")

# Mount websocket app
app.mount("/", socketio.ASGIApp(sio))

@app.get("/")
async def root():
    return {"status": "chat backend running"}