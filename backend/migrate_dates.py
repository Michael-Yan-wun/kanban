from sqlalchemy import create_engine, text
from app.database import SQLALCHEMY_DATABASE_URL
import os

# 確保 URL 正確 (如果需要從環境變數讀取)
if not SQLALCHEMY_DATABASE_URL:
    print("Error: SQLALCHEMY_DATABASE_URL not found.")
    exit(1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def run_migration():
    print("Start migration: Adding date columns to tickets table...")
    with engine.connect() as connection:
        try:
            # 使用 text() 包裝 SQL 語句
            connection.execute(text("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS start_date TIMESTAMP WITH TIME ZONE;"))
            connection.execute(text("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;"))
            connection.commit()
            print("Migration successful! Added start_date and due_date columns.")
        except Exception as e:
            print(f"Migration failed: {e}")

if __name__ == "__main__":
    run_migration()
