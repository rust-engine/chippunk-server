import bcrypt
from fastapi import APIRouter, HTTPException, FastAPI
from utils.db import get_db
from pydantic import BaseModel
import secrets

router = APIRouter()
app = FastAPI()

# Declare what data we need, and in which type.
class LoginData(BaseModel):
    username: str
    password: str


# Login function starts here
@router.post("/login", tags=["auth"])
def login(user: LoginData):
    # We use 
    db = get_db()
    cur = db.cursor()

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)

    cur.execute("SELECT id, password FROM users WHERE username = ?", (user.username,))
    row = cur.fetchone()

    user_id = row[0]
    stored_password = row[1].encode("utf-8")

    if not bcrypt.checkpw(user.password.encode("utf-8"), stored_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = secrets.token_urlsafe(32)
    cur.execute("INSERT INTO sessions (user_id, token) VALUES (?, ?)", (user_id, token))
    db.commit()

    return {"auth_id": user_id, "token": token}