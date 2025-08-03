import sqlite3
import bcrypt
from typing import Optional, List, Dict, Any
from config import Config
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database manager for user operations"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
    
    def get_connection(self):
        """Get database connection with proper error handling"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def init_database(self):
        """Initialize database with proper schema"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
                logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(Config.SALT_ROUNDS)).decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def create_user(self, name: str, email: str, password: str) -> Dict[str, Any]:
        """Create a new user with hashed password"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                password_hash = self.hash_password(password)
                
                cursor.execute(
                    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                    (name, email, password_hash)
                )
                conn.commit()
                
                user_id = cursor.lastrowid
                logger.info(f"User created successfully with ID: {user_id}")
                
                return {
                    "id": user_id,
                    "name": name,
                    "email": email,
                    "created_at": self._get_timestamp()
                }
        except sqlite3.IntegrityError:
            raise ValueError("Email already exists")
        except sqlite3.Error as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                user = cursor.fetchone()
                
                if user:
                    return dict(user)
                return None
        except sqlite3.Error as e:
            logger.error(f"Error getting user by ID: {e}")
            raise
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                user = cursor.fetchone()
                
                if user:
                    return dict(user)
                return None
        except sqlite3.Error as e:
            logger.error(f"Error getting user by email: {e}")
            raise
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users (excluding password hashes)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, email, created_at, updated_at FROM users")
                users = cursor.fetchall()
                
                return [dict(user) for user in users]
        except sqlite3.Error as e:
            logger.error(f"Error getting all users: {e}")
            raise
    
    def update_user(self, user_id: int, name: str = None, email: str = None) -> Optional[Dict[str, Any]]:
        """Update user information"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Build update query dynamically
                update_fields = []
                params = []
                
                if name is not None:
                    update_fields.append("name = ?")
                    params.append(name)
                
                if email is not None:
                    update_fields.append("email = ?")
                    params.append(email)
                
                if not update_fields:
                    return None
                
                update_fields.append("updated_at = CURRENT_TIMESTAMP")
                params.append(user_id)
                
                query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
                
                if cursor.rowcount > 0:
                    return self.get_user_by_id(user_id)
                return None
        except sqlite3.IntegrityError:
            raise ValueError("Email already exists")
        except sqlite3.Error as e:
            logger.error(f"Error updating user: {e}")
            raise
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                
                deleted = cursor.rowcount > 0
                if deleted:
                    logger.info(f"User {user_id} deleted successfully")
                
                return deleted
        except sqlite3.Error as e:
            logger.error(f"Error deleting user: {e}")
            raise
    
    def search_users_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search users by name (case-insensitive)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, name, email, created_at, updated_at FROM users WHERE name LIKE ?",
                    (f"%{name}%",)
                )
                users = cursor.fetchall()
                
                return [dict(user) for user in users]
        except sqlite3.Error as e:
            logger.error(f"Error searching users: {e}")
            raise
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        try:
            user = self.get_user_by_email(email)
            if user and self.verify_password(password, user['password_hash']):
                # Return user data without password hash
                return {
                    "id": user['id'],
                    "name": user['name'],
                    "email": user['email'],
                    "created_at": user['created_at']
                }
            return None
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat() 