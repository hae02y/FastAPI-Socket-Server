# app/database_sync.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 예: MariaDB 연결 URL
DATABASE_URL = "mariadb+pymysql://url"

# 동기 엔진
engine = create_engine(DATABASE_URL,
                       pool_pre_ping=True,
                       pool_recycle=28000,
                       pool_size=10,
                       max_overflow=20,
                       connect_args={
                           "charset": "utf8mb4",
                           "autocommit": False
                       })

# 세션팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
