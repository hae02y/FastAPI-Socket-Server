from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from app.service.status_save_service import start_status_saver
from app.socket.server import start_tcp_server
from app.service.status_sender_service import start_status_sender
from app.api import polygon

app = FastAPI()
app.include_router(polygon.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup_event():
    start_tcp_server()
    start_status_saver()
    # start_status_sender()