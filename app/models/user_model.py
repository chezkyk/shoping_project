from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.postgres_connection import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)

    # Relationship with groups
    groups = relationship('Group',
                          secondary='user_groups',
                          back_populates='users')
