from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from .jwt import create_access_token

router = APIRouter()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# TEMP fake user db
users = {}

@router.post("/register")
async def register(data: dict):
    email = data["email"]
    password = pwd_context.hash(data["password"])

    users[email] = {"email": email, "password": password}
    return {"message": "User registered"}

@router.post("/login")
async def login(data: dict):
    email = data["email"]
    password = data["password"]

    user = users.get(email)
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": email})

    return {"access_token": token, "token_type": "bearer"}
