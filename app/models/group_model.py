from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    # Relationship with users
    users = relationship('User',
                         secondary='user_groups',
                         back_populates='groups')
