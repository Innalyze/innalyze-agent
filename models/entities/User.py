import os
from datetime import datetime

from loguru import logger
from sqlalchemy import Column, String, Integer, Boolean, DateTime

# Do not remove this import, it is required for SQLAlchemy
try:
    pass
    # from models.entities.Feedback import Feedback
    # from models.entities.Rating import Rating
    # from models.entities.Request import Request
    # from models.entities.Token import Token
except ImportError as e:
    logger.warning(f"{os.path.basename(__file__)}: {e.msg}")

from base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True)
    fullname = Column(String(100))
    password = Column(String(100), nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(), default=datetime.now)