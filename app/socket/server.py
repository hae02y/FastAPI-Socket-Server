import socket, os
from threading import Thread
from app.service.packet_parser_service import parse_packet
from datetime import datetime
from app.service.status_store_service import save_status

LISTEN_PORT = 5448

def handle_client(conn, addr):

    with conn:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [연결됨] {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [수신 {addr}] {data}")
            parsed = parse_packet(data)
            if parsed:
                for parse_item in parsed["status_details"]:
                    save_status(parsed["ccm_num"], parsed["scm_num"], parse_item["index"], parse_item["status"])

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