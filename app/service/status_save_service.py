# app/service/status_save_service.py
# app/service/status_sender.py
import threading
import time
from app.service.status_store_service import get_recent_status
from app.repo.slot_repo import save_statuses

ENABLE = True
SEND_INTERVAL = 10  # seconds

def send_statuses():
    while True:
        time.sleep(SEND_INTERVAL)

        data = get_recent_status()
        if not data:
            continue

        try:
            updated = save_statuses(data)  # <-- 여기서 DB로 바로 저장
            print(data)
            print(f"[DB 전송됨] 요청 {len(data)}건 / 실제 갱신 {updated}건")
        except Exception as e:
            print(f"[에러] 상태 DB 저장 실패: {e}")

def test_sender():
    while True:
        time.sleep(SEND_INTERVAL)
        data = get_recent_status()
        print(data)
        print(f"[전송(dry-run)] {len(data)}건")

def start_status_saver():
    target = send_statuses if ENABLE else test_sender
    thread = threading.Thread(target=target, daemon=True)
    thread.start()