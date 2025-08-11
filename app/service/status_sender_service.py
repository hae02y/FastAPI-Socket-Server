# app/service/status_sender.py
import threading
import time
import requests
from app.service.status_store_service import get_recent_status

ENABLE = True
SEND_INTERVAL = 10  # seconds
TARGET_API_URL = "http://3.36.66.196:8082/gateway/PKL2507310000001/slots"

def send_statuses():
    while True:
        time.sleep(SEND_INTERVAL)

        data = get_recent_status()
        if not data:
            continue

        headers = {
            "Content-Type": "application/json",
            "Authorization" : "Key"
        }

        try:
            response = requests.put(TARGET_API_URL, headers=headers ,json=data)
            print(f"[전송됨] {len(data)}건 / 응답: {response.text}")
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