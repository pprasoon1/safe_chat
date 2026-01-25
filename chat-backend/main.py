from fastapi import FastAPI
import socketio
from chat.sockets import sio
from auth.routes import router as auth_router
from routes.rooms import router as rooms_router
from fastapi.middleware.cors import CORSMiddleware

from db import engine, Base   # 👈 IMPORTANT: import these

app = FastAPI()

# 🔥 AUTO-CREATE TABLES ON STARTUP (THIS FIXES YOUR ERROR)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables ensured")

# 🌍 CORS (allow Render + Vercel later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://safechat-azure.vercel.app",  
        "https://safe-chat-ovd9.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST auth routes
app.include_router(auth_router, prefix="/auth")
# REST room routes
app.include_router(rooms_router, prefix="/rooms")

# Mount websocket app (VERY IMPORTANT: mount AFTER routers)
app.mount("/socket.io", socketio.ASGIApp(sio))

@app.get("/")
async def root():
    return {"status": "chat backend running"}
