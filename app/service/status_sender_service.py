# app/service/status_sender.py
import threading
import time
import requests
from app.service.status_store_service import get_recent_status

ENABLE = False
SEND_INTERVAL = 1  # seconds
TARGET_API_URL = "http://your-api-server.com/api/update-status"

def send_statuses():
    while True:
        time.sleep(SEND_INTERVAL)

        data = get_recent_status()
        if not data:
            continue

        try:
            response = requests.post(TARGET_API_URL, json=data)
            print(f"[전송됨] {len(data)}건 / 응답: {response.status_code}")
        except Exception as e:
            print(f"[에러] 상태 전송 실패: {e}")

def test_sender():
    while True:
        time.sleep(SEND_INTERVAL)
        data = get_recent_status()
        print(data)
        print(f"[전송됨] {len(data)}건")

def start_status_sender():
    if ENABLE:
        thread = threading.Thread(target=send_statuses, daemon=True)
        thread.start()
    else:
        thread = threading.Thread(target=test_sender, daemon=True)
        thread.start()