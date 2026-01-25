# 🐳 SafeChat AI — Full Docker & Docker‑Compose Setup

This guide lets you run the **entire SafeChat AI platform** (Frontend + Chat Backend + ML Service + PostgreSQL + Redis) using a **single command**:

```
docker-compose up --build
```

---

## 🏗️ Services We Will Run

- 🖥️ Next.js Frontend  
- 💬 FastAPI Chat Backend (Socket.IO + REST)  
- 🧠 ML Toxicity Service  
- 🗄️ PostgreSQL Database  
- 🔴 Redis (pub/sub, presence, typing)

All containers run on the same Docker network and communicate internally.

---

## 📂 Final Folder Layout (Recommended)

```
safe-chat/
├── docker-compose.yml
│
├── chat-backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
│
├── ml-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── ...
```

---

# 🔹 1. CHAT BACKEND DOCKERFILE

Create: `chat-backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# 🔹 2. ML SERVICE DOCKERFILE

Create: `ml-service/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
```

---

# 🔹 3. FRONTEND DOCKERFILE (Next.js App Router)

Create: `frontend/Dockerfile`

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]
```

---

# 🔹 4. DOCKER‑COMPOSE FILE (MAIN MAGIC 🔥)

Create in root: `docker-compose.yml`

```yaml
version: "3.9"

services:

  # 🔴 Redis
  redis:
    image: redis:7
    container_name: safechat-redis
    ports:
      - "6379:6379"


  # 🗄️ PostgreSQL
  postgres:
    image: postgres:15
    container_name: safechat-postgres
    environment:
      POSTGRES_USER: safechat
      POSTGRES_PASSWORD: safechat
      POSTGRES_DB: safechat
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data


  # 🧠 ML Moderation Service
  ml-service:
    build: ./ml-service
    container_name: safechat-ml
    ports:
      - "8001:8001"
    depends_on:
      - redis


  # 💬 Chat Backend (FastAPI + Socket.IO)
  chat-backend:
    build: ./chat-backend
    container_name: safechat-backend
    ports:
      - "8000:8000"
    depends_on:
      - redis
      - postgres
      - ml-service
    environment:
      DATABASE_URL: postgresql+asyncpg://safechat:safechat@postgres:5432/safechat
      REDIS_URL: redis://redis:6379
      ML_URL: http://ml-service:8001/predict


  # 🖥️ Frontend (Next.js)
  frontend:
    build: ./frontend
    container_name: safechat-frontend
    ports:
      - "3000:3000"
    depends_on:
      - chat-backend


volumes:
  postgres_data:
```

---

# 🔹 5. IMPORTANT BACKEND CONFIG CHANGES

### 🔥 Update Redis Client

In `redis_client.py`:

```python
import redis.asyncio as redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)
```

---

### 🔥 Update Database Engine

In `db.py`:

```python
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://safechat:safechat@localhost/safechat"
)

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

---

### 🔥 Update ML Pipeline URL

In `moderation/pipeline.py`:

```python
import os

ML_URL = os.getenv("ML_URL", "http://localhost:8001/predict")
```

---

# 🔹 6. FRONTEND SOCKET CONFIG (DOCKER‑READY)

In `frontend/lib/socket.ts`:

```ts
import { io } from "socket.io-client";
import { getToken } from "./auth";

export function createSocket() {
  const token = getToken();

  return io("http://localhost:8000", {
    auth: { token },
    transports: ["websocket"]
  });
}
```

---

# 🚀 RUN THE FULL SYSTEM

From project root:

```bash
docker-compose up --build
```

This will start:

| Service | URL |
|--------|-----|
| Frontend | http://localhost:3000 |
| Chat Backend | http://localhost:8000 |
| ML Service | http://localhost:8001 |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

---

# 🧪 FIRST‑TIME SETUP (CREATE TABLES)

After containers start, open another terminal:

```bash
docker exec -it safechat-backend bash
python create_tables.py
exit
```

---

# 🛑 STOP SYSTEM

```bash
docker-compose down
```

To also delete DB data:

```bash
docker-compose down -v
```

---

# 👑 WHAT YOU ACHIEVED

You now have:

- ✅ Fully containerized microservices system  
- ✅ One‑command startup  
- ✅ Redis + Postgres production topology  
- ✅ Scalable Socket.IO infra  
- ✅ ML inference as independent service  

This is **enterprise‑grade architecture**.

---

# 🔥 NEXT UPGRADE OPTIONS

- Kubernetes manifests  
- Nginx reverse proxy  
- Production env variables & secrets  
- Deployment to Railway / Render / Fly.io  

---

🚀 SafeChat AI is now cloud‑ready 🔥

