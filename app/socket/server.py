import socket, os
from threading import Thread
from app.service.packet_parser_service import parse_packet

LISTEN_PORT = os.environ.get('LISTEN_PORT')

def handle_client(conn, addr):
    with conn:
        print(f"[연결됨] {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[수신 {addr}] {data}")
            parsed = parse_packet(data)
            if parsed:
                print(parsed)

def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", LISTEN_PORT))
    server_socket.listen(5)
    print(f"[TCP] Listening on {LISTEN_PORT} ...")
    while True:
        conn, addr = server_socket.accept()
        Thread(target=handle_client, args=(conn, addr), daemon=True).start()

def start_tcp_server():
    Thread(target=tcp_server, daemon=True).start()