from fastapi import HTTPException, Request
from utils.db import get_db

# Verify player's token and ID, just to make sure there was no tomfoolery with them both.
def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    # If client didn't send us an auth header, or 'bad' one - just decline it.
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")

    token = auth_header.split("Bearer ")[1]

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT user_id FROM sessions WHERE token = ?", (token))
    row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="Invalid token. Login again.")

    return row[0]