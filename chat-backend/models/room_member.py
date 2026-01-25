from sqlalchemy import Column, Integer, ForeignKey
from db import Base

class RoomMember(Base):
    __tablename__ = "room_members"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    