from fastapi import APIRouter, HTTPException, FastAPI, Depends
from utils.db import get_db
from pydantic import BaseModel
from utils.auth import verify_token

router = APIRouter()
app = FastAPI()

class CharacterCreatorData(BaseModel):
    #
    name: str
    age: int
    corp: str
    strength: str
    intelligence: str
    stature: str


@router.post("/create", tags=["character"])
def create_character(user: CharacterCreatorData, user_id: str=Depends(verify_token)):
    db = get_db()
    cur = db.cursor()

    # Verify corporation

    corporations = cur.execute("SELECT name FROM corporations")
    if user.corp in corporations:
        pass
    else:
        raise HTTPException(status_code=418, detail="Invalid credentials")

