from fastapi import FastAPI
from app.socket.server import start_tcp_server

app = FastAPI()
# app.include_router(health.router)

@app.on_event("startup")
def startup_event():
    start_tcp_server()