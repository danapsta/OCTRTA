from fastapi import FastAPI
from .routers import google, outlook, apple

app = FastAPI()

app.include_router(google.router, prefix="/google")
app.include_router(outlook.router, prefix="/outlook")
app.include_router(apple.router, prefix="/apple")

@app.get("/")
def read_root():
    return {"message": "Calendar Sync API is running"}
