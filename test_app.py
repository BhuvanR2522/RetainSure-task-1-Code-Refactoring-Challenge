import pytest
import json
from app import app
from database import DatabaseManager
import tempfile
import os
import time

class TestUserManagementAPI:
    """Test cases for the User Management API"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        # Use temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        
        # Update config to use temporary database
        from config import Config
        Config.DATABASE_PATH = self.db_path
        
        # Initialize test database
        self.db_manager = DatabaseManager(self.db_path)
        self.db_manager.init_database()
        
        # Create test client
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        yield
        
        # Cleanup - wait a bit to ensure connections are closed
        try:
            time.sleep(0.1)
            if os.path.exists(self.db_path):
                os.unlink(self.db_path)
        except PermissionError:
            # File might still be in use, that's okay for tests
            pass
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
    
    def test_create_user_success(self):
        """Test successful user creation"""
        user_data = {
            "name": "Test User",
            "email": "test1@testdomain.org",  # Using a unique email
            "password": "testpass123"
        }
        
        response = self.client.post('/users', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == user_data['name']
        assert data['data']['email'] == user_data['email']
        assert 'id' in data['data']
    
    def test_create_user_invalid_data(self):
        """Test user creation with invalid data"""
        # Missing required fields
        user_data = {"name": "Test User"}
        
        response = self.client.post('/users',
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_create_user_weak_password(self):
        """Test user creation with weak password"""
        user_data = {
            "name": "Test User",
            "email": "test@testdomain.org",
            "password": "123"  # Too short
        }
        
        response = self.client.post('/users',
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_get_all_users(self):
        """Test getting all users"""
        # Create a test user first
        user_data = {
            "name": "Test User",
            "email": "test2@testdomain.org",
            "password": "testpass123"
        }
        self.client.post('/users',
                        data=json.dumps(user_data),
                        content_type='application/json')
        
        response = self.client.get('/users')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']) >= 1
    
    def test_get_user_by_id(self):
        """Test getting user by ID"""
        # Create a test user first
        user_data = {
            "name": "Test User",
            "email": "test3@testdomain.org",
            "password": "testpass123"
        }
        create_response = self.client.post('/users',
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        user_id = json.loads(create_response.data)['data']['id']
        
        response = self.client.get(f'/user/{user_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == user_data['name']
    
    def test_get_user_not_found(self):
        """Test getting non-existent user"""
        response = self.client.get('/user/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_login_success(self):
        """Test successful login"""
        # Create a test user first
        user_data = {
            "name": "Test User",
            "email": "test4@testdomain.org",
            "password": "testpass123"
        }
        self.client.post('/users',
                        data=json.dumps(user_data),
                        content_type='application/json')
        
        login_data = {
            "email": "test4@testdomain.org",
            "password": "testpass123"
        }
        
        response = self.client.post('/login',
                                  data=json.dumps(login_data),
                                  content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['email'] == login_data['email']
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            "email": "nonexistent@testdomain.org",
            "password": "wrongpassword"
        }
        
        response = self.client.post('/login',
                                  data=json.dumps(login_data),
                                  content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_search_users(self):
        """Test user search functionality"""
        # Create test users
        users = [
            {"name": "John Doe", "email": "john@testdomain.org", "password": "pass123"},
            {"name": "Jane Smith", "email": "jane@testdomain.org", "password": "pass456"},
            {"name": "Bob Johnson", "email": "bob@testdomain.org", "password": "pass789"}
        ]
        
        for user in users:
            self.client.post('/users',
                           data=json.dumps(user),
                           content_type='application/json')
        
        response = self.client.get('/search?name=John')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['data']) >= 1
    
    def test_update_user(self):
        """Test user update functionality"""
        # Create a test user first
        user_data = {
            "name": "Test User",
            "email": "test5@testdomain.org",
            "password": "testpass123"
        }
        create_response = self.client.post('/users',
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        user_id = json.loads(create_response.data)['data']['id']
        
        # Update user
        update_data = {
            "name": "Updated User",
            "email": "updated@testdomain.org"
        }
        
        response = self.client.put(f'/user/{user_id}',
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['name'] == update_data['name']
        assert data['data']['email'] == update_data['email']
    
    def test_delete_user(self):
        """Test user deletion"""
        # Create a test user first
        user_data = {
            "name": "Test User",
            "email": "test6@testdomain.org",
            "password": "testpass123"
        }
        create_response = self.client.post('/users',
                                         data=json.dumps(user_data),
                                         content_type='application/json')
        user_id = json.loads(create_response.data)['data']['id']
        
        # Delete user
        response = self.client.delete(f'/user/{user_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        
        # Verify user is deleted
        get_response = self.client.get(f'/user/{user_id}')
        assert get_response.status_code == 404

if __name__ == '__main__':
    # Run basic functionality test
    print("Testing User Management API...")
    
    # This would run the tests if pytest is available
    # pytest.main([__file__])
    
    print("Test file created successfully. Run with: pytest test_app.py") 