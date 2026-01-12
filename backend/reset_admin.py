from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models, crud
import sys

def reset_admin():
    db = SessionLocal()
    try:
        username = "admin"
        new_password = "admin123"
        
        user = crud.get_user_by_username(db, username=username)
        if not user:
            print(f"❌ User '{username}' not found!")
            return

        # 更新密碼
        hashed_pw = crud.get_password_hash(new_password)
        user.password_hash = hashed_pw
        user.role = "admin"  # 確保是管理員
        db.commit()
        
        print(f"✅ User '{username}' password reset to '{new_password}'")
        print(f"✅ User role set to 'admin'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin()
