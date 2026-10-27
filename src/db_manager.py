import sqlite3
import hashlib
import os

class DatabaseManager:
    def __init__(self, db_path="data/users.db"):
        self.db_path = db_path
        self._ensure_data_dir()
        self._init_db()
        self._migrate_db()

    def _ensure_data_dir(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Create table with new schema if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                mobile_number TEXT,
                gender TEXT,
                user_type TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _migrate_db(self):
        """Check for missing columns and add them if necessary."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            # Check if new columns exist
            cursor.execute("SELECT full_name, email, mobile_number, gender, user_type FROM users LIMIT 1")
        except sqlite3.OperationalError:
            # Columns missing, add them
            print("Migrating database schema...")
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
            except: pass
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
            except: pass
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN mobile_number TEXT")
            except: pass
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN gender TEXT")
            except: pass
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN user_type TEXT")
            except: pass
            conn.commit()
        finally:
            conn.close()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password, full_name, email, mobile_number, gender, user_type):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            pwd_hash = self._hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, password_hash, full_name, email, mobile_number, gender, user_type) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, pwd_hash, full_name, email, mobile_number, gender, user_type))
            conn.commit()
            conn.close()
            return True, "User registered successfully!"
        except sqlite3.IntegrityError:
            return False, "Username already exists."
        except Exception as e:
            return False, f"Error: {str(e)}"

    def validate_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        pwd_hash = self._hash_password(password)
        cursor.execute("SELECT password_hash, user_type FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] == pwd_hash:
            return True, "Login successful!", result[1] # Return user_type as well
        else:
            return False, "Invalid username or password.", None
