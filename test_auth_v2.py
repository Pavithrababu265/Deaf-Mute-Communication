from src.db_manager import DatabaseManager
import os

def test_auth_v2():
    # Setup clean test 
    test_db = "data/test_users_v2.db"
    if os.path.exists(test_db):
        os.remove(test_db)
        
    db = DatabaseManager(test_db)
    
    # 1. Register User (New Schema)
    success, msg = db.add_user("echo_user", "securepass", "Echo User", "user@echo.com", "Normal")
    print(f"Register Full: {success} - {msg}")
    if not success: return False
    
    # 2. Login Success
    success, msg = db.validate_user("echo_user", "securepass")
    print(f"Login Success: {success} - {msg}")
    if not success: return False
    
    # Cleanup
    if os.path.exists(test_db):
        os.remove(test_db)
        
    return True

if __name__ == "__main__":
    if test_auth_v2():
        print("ALL TESTS PASSED (V2)")
    else:
        print("TESTS FAILED (V2)")
