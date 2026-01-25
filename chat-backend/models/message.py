from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from db import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, index= True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    toxicity= Column(Float)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
