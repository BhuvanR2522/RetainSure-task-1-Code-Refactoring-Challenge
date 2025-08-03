from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import json
from typing import Dict, Any, Tuple

from config import Config
from database import DatabaseManager
from validators import UserValidator, ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Initialize database manager
db_manager = DatabaseManager()

def create_error_response(message: str, status_code: int = 400) -> Tuple[Dict[str, Any], int]:
    """Create standardized error response"""
    return {
        "error": message,
        "status": "error"
    }, status_code

def create_success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    """Create standardized success response"""
    response = {
        "status": "success",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response

@app.route('/')
def health_check():
    """Health check endpoint"""
    return create_success_response(message="User Management System is running")

@app.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    try:
        users = db_manager.get_all_users()
        return create_success_response(data=users, message="Users retrieved successfully")
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return create_error_response("Failed to retrieve users", 500)

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user by ID"""
    try:
        # Validate user ID
        validated_user_id = UserValidator.validate_user_id(user_id)
        
        # Get user from database
        user = db_manager.get_user_by_id(validated_user_id)
        
        if user:
            # Remove password hash from response
            user.pop('password_hash', None)
            return create_success_response(data=user, message="User retrieved successfully")
        else:
            return create_error_response("User not found", 404)
            
    except ValidationError as e:
        return create_error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        return create_error_response("Failed to retrieve user", 500)

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        # Get and validate request data
        if not request.is_json:
            return create_error_response("Content-Type must be application/json", 400)
        
        data = request.get_json()
        validated_data = UserValidator.validate_create_user_data(data)
        
        # Create user in database
        user = db_manager.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        response_data = create_success_response(data=user, message="User created successfully")
        return jsonify(response_data), 201
        
    except ValidationError as e:
        return create_error_response(str(e), 400)
    except ValueError as e:
        return create_error_response(str(e), 409)  # Conflict for duplicate email
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return create_error_response("Failed to create user", 500)

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    try:
        # Validate user ID
        validated_user_id = UserValidator.validate_user_id(user_id)
        
        # Get and validate request data
        if not request.is_json:
            return create_error_response("Content-Type must be application/json", 400)
        
        data = request.get_json()
        validated_data = UserValidator.validate_update_user_data(data)
        
        # Update user in database
        updated_user = db_manager.update_user(
            user_id=validated_user_id,
            name=validated_data.get('name'),
            email=validated_data.get('email')
        )
        
        if updated_user:
            # Remove password hash from response
            updated_user.pop('password_hash', None)
            return create_success_response(data=updated_user, message="User updated successfully")
        else:
            return create_error_response("User not found", 404)
            
    except ValidationError as e:
        return create_error_response(str(e), 400)
    except ValueError as e:
        return create_error_response(str(e), 409)  # Conflict for duplicate email
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        return create_error_response("Failed to update user", 500)

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user by ID"""
    try:
        # Validate user ID
        validated_user_id = UserValidator.validate_user_id(user_id)
        
        # Delete user from database
        deleted = db_manager.delete_user(validated_user_id)
        
        if deleted:
            return create_success_response(message="User deleted successfully")
        else:
            return create_error_response("User not found", 404)
            
    except ValidationError as e:
        return create_error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        return create_error_response("Failed to delete user", 500)

@app.route('/search', methods=['GET'])
def search_users():
    """Search users by name"""
    try:
        # Get and validate search parameter
        name = request.args.get('name')
        if not name:
            return create_error_response("Name parameter is required", 400)
        
        validated_name = UserValidator.validate_search_name(name)
        
        # Search users in database
        users = db_manager.search_users_by_name(validated_name)
        
        return create_success_response(data=users, message="Search completed successfully")
        
    except ValidationError as e:
        return create_error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error searching users: {e}")
        return create_error_response("Failed to search users", 500)

@app.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        # Get and validate request data
        if not request.is_json:
            return create_error_response("Content-Type must be application/json", 400)
        
        data = request.get_json()
        validated_data = UserValidator.validate_login_data(data)
        
        # Authenticate user
        user = db_manager.authenticate_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        if user:
            return create_success_response(data=user, message="Login successful")
        else:
            return create_error_response("Invalid email or password", 401)
            
    except ValidationError as e:
        return create_error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return create_error_response("Failed to authenticate user", 500)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return create_error_response("Endpoint not found", 404)

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return create_error_response("Method not allowed", 405)

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return create_error_response("Internal server error", 500)

if __name__ == '__main__':
    # Initialize database
    try:
        db_manager.init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        exit(1)
    
    # Start the application
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )