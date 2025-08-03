from database import DatabaseManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize database with sample data"""
    try:
        db_manager = DatabaseManager()
        
        # Initialize database schema
        db_manager.init_database()
        
        # Add sample users with hashed passwords
        sample_users = [
            {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "password123"
            },
            {
                "name": "Jane Smith", 
                "email": "jane@example.com",
                "password": "secret456"
            },
            {
                "name": "Bob Johnson",
                "email": "bob@example.com", 
                "password": "qwerty789"
            }
        ]
        
        for user_data in sample_users:
            try:
                db_manager.create_user(
                    name=user_data["name"],
                    email=user_data["email"],
                    password=user_data["password"]
                )
                logger.info(f"Created user: {user_data['name']}")
            except ValueError as e:
                logger.warning(f"User {user_data['email']} already exists: {e}")
        
        logger.info("Database initialized successfully with sample data")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

if __name__ == "__main__":
    init_database()