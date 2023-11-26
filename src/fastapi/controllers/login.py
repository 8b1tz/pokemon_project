from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import secrets
from fastapi import Depends, Header, HTTPException
import bcrypt
from datetime import datetime, timedelta
from models.usuario import User, UserModel, PostCreate
import jwt
from typing import Optional

SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"
SQLALCHEMY_DATABASE_URL = "sqlite:///./usuarios_teste.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_user(db, user: User):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
    hashed_password = hash_password(user.password)
    token = secrets.token_urlsafe(32)
    current_datetime = datetime.utcnow()

    db_user = UserModel(username=user.username, password=hashed_password,
                        token=token, last_login=current_datetime)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"username": db_user.username, "token": db_user.token}

async def get_access_token(cookie: Optional[str] = None):
    if cookie is None:
        raise HTTPException(status_code=401, detail="Token não fornecido corretamente")

    return cookie
async def get_token_autenticado(token: str = Depends(get_access_token)):
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")
        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return usuario
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def get_user_by_username(db, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_post(db: Session, user_id: int, post: PostCreate):
    db_post = Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def add_friend(db: Session, user_id: int, friend_id: int):
    friendship = Friendship(user_id=user_id, friend_id=friend_id)
    db.add(friendship)
    db.commit()
    return friendship

# Remover um amigo de um usuário
def remove_friend(db: Session, user_id: int, friend_id: int):
    friendship = db.query(Friendship).filter(
        Friendship.user_id == user_id,
        Friendship.friend_id == friend_id
    ).first()
    if friendship:
        db.delete(friendship)
        db.commit()
        return {"message": "Amigo removido com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Amigo não encontrado")

# Remover um post de um usuário
def delete_post(db: Session, user_id: int, post_id: int):
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == user_id
    ).first()
    if post:
        db.delete(post)
        db.commit()
        return {"message": "Post removido com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Post não encontrado")
