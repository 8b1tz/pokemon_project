from passlib.context import CryptContext
from fastapi import HTTPException
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Autenticação de senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Verificação do usuário
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    return user
