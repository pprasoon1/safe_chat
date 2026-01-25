# models/user.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base   # 🔥 IMPORT BASE FROM db.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
