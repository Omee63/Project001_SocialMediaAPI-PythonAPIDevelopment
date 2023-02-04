from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text


class Post(Base):  # SqlAlchemy Model
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_ad = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(Base):  # 'Base' class extension is required for SqlAlchemy model
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_ad = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
