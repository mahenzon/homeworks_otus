import os

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

PG_CONN_URI = os.environ.get("PG_CONN_URI") or "postgresql://postgres:password@localhost/postgres"
engine = create_engine(PG_CONN_URI)

Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    username = Column(String(64), unique=True)
    email = Column(String(64), unique=True)
    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(256), nullable=False)
    body = Column(Text, nullable=False)
    user = relationship(User, back_populates="posts")
