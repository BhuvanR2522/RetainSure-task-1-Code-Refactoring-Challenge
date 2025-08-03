import re
from typing import Dict, Any, Optional
from email_validator import validate_email, EmailNotValidError

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class UserValidator:
    """Validator for user data"""
    
    @staticmethod
    def validate_email(email: str) -> str:
        """Validate and normalize email address"""
        if not email or not isinstance(email, str):
            raise ValidationError("Email is required and must be a string")
        
        email = email.strip().lower()
        
        try:
            validated_email = validate_email(email)
            return validated_email.normalized
        except EmailNotValidError as e:
            raise ValidationError(f"Invalid email format: {str(e)}")
    
    @staticmethod
    def validate_name(name: str) -> str:
        """Validate user name"""
        if not name or not isinstance(name, str):
            raise ValidationError("Name is required and must be a string")
        
        name = name.strip()
        
        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long")
        
        if len(name) > 100:
            raise ValidationError("Name must be less than 100 characters")
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError("Name can only contain letters, spaces, hyphens, and apostrophes")
        
        return name
    
    @staticmethod
    def validate_password(password: str) -> str:
        """Validate password strength"""
        if not password or not isinstance(password, str):
            raise ValidationError("Password is required and must be a string")
        
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        if len(password) > 128:
            raise ValidationError("Password must be less than 128 characters")
        
        # Check for at least one letter and one number
        if not re.search(r"[a-zA-Z]", password):
            raise ValidationError("Password must contain at least one letter")
        
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one number")
        
        return password
    
    @staticmethod
    def validate_user_id(user_id: str) -> int:
        """Validate user ID"""
        if not user_id:
            raise ValidationError("User ID is required")
        
        try:
            user_id_int = int(user_id)
            if user_id_int <= 0:
                raise ValidationError("User ID must be a positive integer")
            return user_id_int
        except ValueError:
            raise ValidationError("User ID must be a valid integer")
    
    @staticmethod
    def validate_search_name(name: str) -> str:
        """Validate search name parameter"""
        if not name or not isinstance(name, str):
            raise ValidationError("Search name is required and must be a string")
        
        name = name.strip()
        
        if len(name) < 1:
            raise ValidationError("Search name cannot be empty")
        
        if len(name) > 50:
            raise ValidationError("Search name must be less than 50 characters")
        
        # Sanitize search input
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError("Search name can only contain letters, spaces, hyphens, and apostrophes")
        
        return name
    
    @staticmethod
    def validate_create_user_data(data: Dict[str, Any]) -> Dict[str, str]:
        """Validate data for creating a user"""
        if not isinstance(data, dict):
            raise ValidationError("Request data must be a JSON object")
        
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")
        
        validated_data = {
            'name': UserValidator.validate_name(data['name']),
            'email': UserValidator.validate_email(data['email']),
            'password': UserValidator.validate_password(data['password'])
        }
        
        return validated_data
    
    @staticmethod
    def validate_update_user_data(data: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """Validate data for updating a user"""
        if not isinstance(data, dict):
            raise ValidationError("Request data must be a JSON object")
        
        validated_data = {}
        
        if 'name' in data:
            validated_data['name'] = UserValidator.validate_name(data['name'])
        
        if 'email' in data:
            validated_data['email'] = UserValidator.validate_email(data['email'])
        
        if not validated_data:
            raise ValidationError("At least one field (name or email) must be provided for update")
        
        return validated_data
    
    @staticmethod
    def validate_login_data(data: Dict[str, Any]) -> Dict[str, str]:
        """Validate data for user login"""
        if not isinstance(data, dict):
            raise ValidationError("Request data must be a JSON object")
        
        if 'email' not in data:
            raise ValidationError("Email is required for login")
        
        if 'password' not in data:
            raise ValidationError("Password is required for login")
        
        validated_data = {
            'email': UserValidator.validate_email(data['email']),
            'password': data['password']  # Don't validate password format for login
        }
        
        return validated_data 