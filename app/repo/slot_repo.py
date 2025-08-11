from typing import Iterable, Dict, List
from sqlalchemy import text
from app.config.db_config import SessionLocal

SQL_UPDATE_ONE = text("""
UPDATE tb_svp_parking_slot
   SET pks_st = :pks_st,
       pks_st_updated = NOW()
 WHERE pks_seq = :pks_seq
   AND pks_fl = 'AUTO'
""")

def _chunk(iterable: Iterable[Dict], size: int) -> Iterable[List[Dict]]:
    batch: List[Dict] = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch

def save_statuses(status_list: List[Dict], chunk_size: int = 500) -> int:
    """
    status_list: [{"pks_seq": str, "pks_st": str}, ...]
    반환값: 실제로 갱신된 행(row) 수
    """
    if not status_list:
        return 0

    # 입력 방어: 필요한 키만 남기고, 이상치 제거
    cleaned = []
    for s in status_list:
        pks_seq = s.get("pksSeq")
        pks_st  = s.get("pksSt")
        if not pks_seq or not isinstance(pks_seq, str):
            continue
        if not pks_st or not isinstance(pks_st, str):
            continue
        cleaned.append({"pks_seq": pks_seq, "pks_st": pks_st})

    if not cleaned:
        return 0

    total_updated = 0
    with SessionLocal() as db:
        try:
            for batch in _chunk(cleaned, chunk_size):
                # executemany: 같은 SQL에 파라미터 리스트 전달
                res = db.execute(SQL_UPDATE_ONE, batch)
                # rowcount는 드라이버에 따라 -1일 수 있으니 방어
                updated = getattr(res, "rowcount", 0) or 0
                total_updated += updated
            db.commit()
        except Exception:
            db.rollback()
            raise
    return total_updated