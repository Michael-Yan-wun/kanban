import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 載入環境變數
load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    print("❌ 錯誤: 找不到 DATABASE_URL，請檢查 .env 檔案")
    exit(1)

print(f"🔄 嘗試連線至: {database_url.split('@')[-1]}") # 只印出後半段避免洩漏密碼

try:
    # 建立引擎
    engine = create_engine(database_url)
    
    # 嘗試執行簡單查詢
    with engine.connect() as connection:
        result = connection.execute(text("SELECT NOW()"))
        current_time = result.scalar()
        print(f"✅ 連線成功！資料庫時間: {current_time}")
        
except Exception as e:
    print(f"❌ 連線失敗: {e}")
