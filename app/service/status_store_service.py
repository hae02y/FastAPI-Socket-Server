from collections import defaultdict, deque
from app.config.pks_map_config import pks_map

status_history = defaultdict(lambda: deque(maxlen=2))

def save_status(ccm, scm, usm, status):
    key = f'{ccm},{scm},{usm}'
    pks_id = pks_map.get(key)
    if pks_id :
        status_history[pks_id].append(status)
        print(f"[{pks_id}] is saved in pks_map.")

def get_recent_status():
    return [
        {"pksSeq" :key, "pksSt" : values[-1]}
        for key, values in status_history.items() if values
    ]