from controllers import create_user
from models import User

from fastapi import FastAPI

app = FastAPI()


@app.post("/register/")
def register_user(user: User):
    return create_user(user)
