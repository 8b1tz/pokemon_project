from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import secrets
from fastapi import Depends, Header, HTTPException
import bcrypt
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class User(BaseModel):
    username: str
    password: str


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int  # Referência ao ID do usuário que cria o post
    

Base = declarative_base()


# Definição da tabela intermediária Friendship
class Friendship(Base):
    __tablename__ = "friendship"
    user_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    friend_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)


class UserModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    token = Column(String)
    last_login = Column(DateTime, default=datetime.utcnow)

    # Relação de amigos
    friends = relationship("UserModel", secondary=Friendship.__table__,
                          primaryjoin=(Friendship.user_id == id),
                          secondaryjoin=(Friendship.friend_id == id),
                          backref="friend_of")

    # Relação de posts
    posts = relationship("Post", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    user = relationship("UserModel", back_populates="posts")
