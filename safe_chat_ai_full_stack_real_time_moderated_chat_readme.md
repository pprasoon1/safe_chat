# 🛡️ SafeChat AI – Real-Time Moderated Chat Platform

SafeChat AI is a **production-grade real-time chat application** with:

- JWT authentication  
- Multi-room & private chats  
- Redis-powered scalable WebSockets  
- PostgreSQL persistence  
- Machine-learning based toxicity detection  
- Automatic moderation (approve / censor / block)  
- Live toxicity meter & typing indicators  

This project demonstrates a **modern microservices architecture** combining FastAPI, Next.js, Redis, PostgreSQL, and an ML inference service.

---

## 🏗️ Architecture Overview

```
Next.js (Frontend)
        │
        ▼
FastAPI Chat Gateway (Socket.IO + REST)
        │
 ┌──────┼────────┐
 │      │        │
 ▼      ▼        ▼
Redis   PostgreSQL   ML Moderation Service
(pub/sub,            (messages, rooms, users)
 online users)
```

Flow:
1. User logs in → receives JWT  
2. Frontend connects via Socket.IO with JWT  
3. Message → FastAPI gateway  
4. Gateway → ML service for toxicity classification  
5. Auto-moderation (approve / censor / block)  
6. Message saved to PostgreSQL  
7. Broadcast via Redis pub/sub to all clients  

---

## 🧰 Tech Stack

### Frontend
- **Next.js 14 (App Router)**  
- **React + TypeScript**  
- **Tailwind CSS**  
- **socket.io-client**  

### Backend (Chat Service)
- **FastAPI**  
- **python-socketio (ASGI)**  
- **Redis (pub/sub, presence, typing)**  
- **PostgreSQL (asyncpg + SQLAlchemy)**  
- **JWT (python-jose)**  
- **bcrypt / passlib**  

### ML Service
- **FastAPI**  
- **scikit-learn / transformers (toxicity model)**  
- **httpx** for service-to-service calls  

---

## 📂 Project Structure

```
safe-chat/
├── chat-backend/        # FastAPI chat gateway + sockets
│   ├── auth/
│   ├── chat/
│   ├── moderation/
│   ├── models/
│   ├── routes/
│   ├── db.py
│   └── main.py
│
├── ml-service/         # Toxicity classification microservice
│   ├── model/
│   ├── app.py
│   └── requirements.txt
│
├── frontend/           # Next.js App Router frontend
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
│
└── README.md
```

---

## ⚙️ Prerequisites

Install the following before starting:

- **Python 3.10+** (recommended: 3.11)  
- **Node.js 18+**  
- **PostgreSQL 14+**  
- **Redis 7+**  

Mac users (with Homebrew):

```bash
brew install postgresql redis
```

---

## 🗄️ Database Setup (PostgreSQL)

Create database:

```bash
psql postgres
CREATE DATABASE safechat;
\q
```

Update your backend `.env` or `db.py` with:

```
DATABASE_URL=postgresql+asyncpg://username:password@localhost/safechat
```

Run table creation script (one time):

```bash
cd chat-backend
python create_tables.py
```

---

## 🔴 Redis Setup

Start Redis server:

```bash
redis-server
```

Check:

```bash
redis-cli ping
# PONG
```

---

## 🧠 ML SERVICE SETUP (Toxicity Classifier)

### 1️⃣ Create virtual environment

```bash
cd ml-service
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run ML service

```bash
uvicorn app:app --port 8001 --reload
```

This service exposes:

```
POST http://localhost:8001/predict
```

---

## 💬 CHAT BACKEND SETUP (FastAPI + Socket.IO)

### 1️⃣ Create virtual environment

```bash
cd chat-backend
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run chat backend

```bash
uvicorn main:app --reload --port 8000
```

Backend endpoints:

- REST: `http://localhost:8000/auth/*`  
- Socket.IO: `http://localhost:8000/socket.io`  

---

## 🖥️ FRONTEND SETUP (Next.js)

### 1️⃣ Install dependencies

```bash
cd frontend
npm install
```

### 2️⃣ Run frontend

```bash
npm run dev
```

Open browser:

```
http://localhost:3000
```

---

## ▶️ FULL STARTUP ORDER (IMPORTANT)

Always start services in this order:

### 1️⃣ Redis

```bash
redis-server
```

### 2️⃣ PostgreSQL

```bash
brew services start postgresql
```

### 3️⃣ ML Service

```bash
cd ml-service
source venv/bin/activate
uvicorn app:app --port 8001 --reload
```

### 4️⃣ Chat Backend

```bash
cd chat-backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### 5️⃣ Frontend

```bash
cd frontend
npm run dev
```

---

## 🔐 Authentication Flow

1. User registers → `/auth/register`  
2. User logs in → `/auth/login`  
3. Backend returns JWT with:

```json
{
  "sub": "user@email.com",
  "user_id": 1
}
```

4. Frontend stores token in `localStorage`  
5. Socket connects with:

```ts
io("http://localhost:8000", { auth: { token } })
```

---

## 💬 Chat Features Implemented

- Global room auto-join  
- Persistent group rooms (PostgreSQL)  
- Private 1-to-1 rooms  
- Typing indicators (room-scoped)  
- Online users (Redis set)  
- Message persistence  
- Room switching UI  

---

## 🧠 AI Moderation Pipeline

For every message:

1. Gateway sends text → ML service  
2. ML returns toxicity score + category  
3. Auto-moderation rules:

| Toxicity | Action |
|----------|--------|
| < 0.3    | Approved |
| 0.3–0.7  | Censored |
| > 0.7    | Blocked |

4. Live toxicity bar updates in UI  
5. Blocked messages never broadcast  

---

## 📊 Socket Events Reference

### Client → Server

- `join_room { room }`  
- `leave_room { room }`  
- `chat_message { room, message, chat_id }`  
- `typing { room }`  
- `start_private_chat { target_user }`  

### Server → Client

- `new_message`  
- `typing`  
- `online_users`  
- `system`  
- `moderation_notice`  
- `toxicity_update`  
- `private_room_created`  

---

## 🧪 Common Issues & Fixes

### ❌ `/socket.io 404`
Make sure in `main.py`:

```python
app.mount("/", socketio.ASGIApp(sio))
```

And frontend connects to:

```ts
io("http://localhost:8000", { transports: ["websocket"] })
```

---

### ❌ `User object is not subscriptable`

Use ORM access:

```python
user.id   # correct
user["id"]  # wrong
```

---

### ❌ Status column float error

Ensure DB schema:

```python
status = Column(String)
```

---

## 🚀 Future Enhancements

- Admin moderation dashboard  
- User risk scoring & auto-mute  
- Room invitations & permissions  
- Message history pagination  
- Docker + docker-compose deployment  
- Cloud deployment (Render / Railway / Fly.io)  

---

## 👑 Final Notes

This project demonstrates:

- Distributed systems design  
- Microservices communication  
- Real-time scalable WebSockets  
- Secure authentication  
- AI in production pipelines  

Perfect for:

- Final year projects  
- Hackathons  
- Portfolio showcase  
- Backend / ML interviews  

---

🔥 Built with FastAPI, Next.js, Redis, PostgreSQL