
import requests
import random
import string

BASE_URL = "http://127.0.0.1:8000"

def random_str(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def run_test():
    username = f"user_{random_str()}"
    password = "password123"
    
    print(f"🚀 開始測試 API... (User: {username})")
    
    # 1. 註冊
    print("[1] 註冊中...")
    resp = requests.post(f"{BASE_URL}/api/auth/register", json={
        "username": username,
        "password": password,
        "name": "Test User",
        "email": f"{username}@test.com"
    })
    if resp.status_code != 200:
        print(f"❌ 註冊失敗: {resp.text}")
        return
    print("✅ 註冊成功")

    # 2. 登入
    print("[2] 登入中...")
    resp = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": username,
        "password": password
    })
    if resp.status_code != 200:
        print(f"❌ 登入失敗: {resp.text}")
        return
    data = resp.json()
    token = data["access_token"]
    print(f"✅ 登入成功! Token: {token[:10]}...")
    
    headers = {"Authorization": f"Token {token}"}
    
    # 3. 建立看板
    print("[3] 建立看板...")
    resp = requests.post(f"{BASE_URL}/api/boards/", headers=headers, json={
        "name": "My First Board",
        "description": "Test board"
    })
    board = resp.json()
    board_id = board["id"]
    print(f"✅ 看板建立成功 ID: {board_id}")
    
    # 4. 取得看板細節 (應自動包含 3 個預設欄位)
    print("[4] 檢查預設欄位...")
    resp = requests.get(f"{BASE_URL}/api/columns/?board_id={board_id}", headers=headers)
    columns = resp.json()
    print(f"✅ 欄位數量: {len(columns)} (預期 3 個)")
    
    if not columns:
        print("❌ 錯誤: 沒有建立預設欄位")
        return
        
    first_col_id = columns[0]["id"]
    
    # 5. 建立 Ticket
    print("[5] 建立 Ticket...")
    resp = requests.post(f"{BASE_URL}/api/tickets/", headers=headers, json={
        "board_id": board_id,
        "column_id": first_col_id,
        "title": "Fix Login Bug",
        "priority": "high"
    })
    ticket = resp.json()
    print(f"✅ Ticket 建立成功 ID: {ticket['id']}, Position: {ticket['position']}")
    
    print("🎉 所有 API 測試通過！")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"❌ 連線錯誤: {e} (確認 Server 是否已啟動?)")
