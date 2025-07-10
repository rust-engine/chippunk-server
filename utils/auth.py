from fastapi import HTTPException, Request
from utils.db import get_db

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")

    token = auth_header.split("Bearer ")[1]

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT user_id FROM sessions WHERE token = ?", (token))
    row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="Invalid user ID or token")

    return row[0]