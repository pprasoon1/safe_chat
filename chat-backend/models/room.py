from sqlalchemy import Column, Integer, String,Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_private = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    create_at = Column(DateTime(timezone=True), server_default=func.now())