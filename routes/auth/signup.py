from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
from utils.db import get_db
import bcrypt

app = FastAPI()
router = APIRouter()

class SignupData(BaseModel):
    username: str
    password: str

@router.post("/signup", tags=["auth"])
def signup(user: SignupData):
    db = get_db()
    cur = db.cursor()

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)

    cur.execute(
        f"SELECT id FROM users WHERE username = ?", (user.username,)
    )
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Username is taken.")

    cur.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_password.decode("utf-8"))
    )
    db.commit()

    return {"message": "Account created successfuly"}