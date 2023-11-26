from controllers.login import create_user, get_access_token, get_token_autenticado, get_db, UserModel, create_access_token, get_user_by_username
from models.usuario import User
from typing import List, Optional
from fastapi import FastAPI, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import bcrypt
from datetime import timedelta
import jwt
from fastapi.responses import JSONResponse

app = FastAPI()
 

@app.post("/register/")
def register_user(user: User, db: Session = Depends(get_db)):
    return create_user(db, user)


@app.post("/login/")
def login_user(user: User, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        if bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
            access_token_expires = timedelta(minutes=30)
            access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")


@app.post("/logout/")
def logout_user(response: Response):
    response.delete_cookie("access_token")  # Remove o token do cliente (exemplo usando cookies)
    return {"message": "Usuário desconectado com sucesso"}


@app.get("/profile/")
async def profile(usuario_logado: str = Depends(get_token_autenticado)):
    return {"usuario_logado": usuario_logado}