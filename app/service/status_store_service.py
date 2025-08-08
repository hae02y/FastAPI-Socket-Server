from collections import defaultdict, deque

status_history = defaultdict(lambda: deque(maxlen=2))

pks_map = {
    "1,1,1" : "PKS2507310000001"
}

def save_status(ccm, scm, usm, status):
    key = f'{ccm},{scm},{usm}'
    pks_id = pks_map.get(key)
    print(f"[{pks_id}] is saved in pks_map.")
    if pks_id :
        status_history[pks_id].append(status)
        print(f"[{pks_id}] is saved in pks_map.")
    else:
        # print(f"[{key}] is not found in pks_map.")
        print("")

def get_recent_status():
    return [
        {"pks" :key, "status" : values[-1]}
        for key, values in status_history.items() if values
    ]