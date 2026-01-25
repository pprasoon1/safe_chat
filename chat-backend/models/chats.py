from sqlalchemy import Boolean, Column, Integer, String
from db import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_group = Column(Boolean, default=False)
