from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.socket.server import start_tcp_server
from app.api import polygon

app = FastAPI()
app.include_router(polygon.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup_event():
    start_tcp_server()