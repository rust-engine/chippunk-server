from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.auth import login, signup
from fastapi.responses import FileResponse
from routes.char import creator
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return FileResponse("public/index.html")


# Auth; Login and Signup
app.include_router(signup.router, prefix="/auth")
app.include_router(login.router, prefix="/auth")

# Character Creator
app.include_router(creator.router)

app.mount("/public", StaticFiles(directory="public"), name="public")

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=80)
