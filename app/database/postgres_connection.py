from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings.config import POSTGRES_CONNECTION
from app.models import Base

user_engine = create_engine(POSTGRES_CONNECTION)

user_session_maker = sessionmaker(bind=user_engine)

Base.metadata.create_all(user_engine)
