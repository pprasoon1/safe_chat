from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db import get_db
from models.user import User
from .jwt import create_access_token

router = APIRouter()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# TEMP fake user db
# users = {}

# REGISTER ROUTE
@router.post("/register")
async def register(data: dict, db: AsyncSession = Depends(get_db)):
    email = data["email"]
    password = data["password"]

    # check if user already exists
    result = await db.execute(select(User).where(User.email == email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    #Hash Password
    hashed_password = pwd_context.hash(password)

    # Create user object
    new_user = User(
        email = email,
        password_hash = hashed_password
    )

    # Save to DB
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "User registered successfully"}

#LOGIN ROUTE
@router.post("/login")
async def login(data: dict, db: AsyncSession = Depends(get_db)):
    email = data["email"]
    password = data["password"]

    #Fetch user from DB
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT
    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}
