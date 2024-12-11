from sqlalchemy import Column, Integer, ForeignKey
from app.models import Base

class UserGroup(Base):
    __tablename__ = 'user_groups'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
