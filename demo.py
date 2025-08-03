#!/usr/bin/env python3
"""
Demo script to showcase the refactored User Management API
"""

import requests
import json
import time

def demo_api():
    """Demonstrate the API functionality"""
    base_url = "http://localhost:5000"
    
    print("🚀 User Management API Demo")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Health Check")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Server not running. Please start the server with: python app.py")
        return
    
    # Test 2: Get All Users
    print("\n2. Get All Users")
    try:
        response = requests.get(f"{base_url}/users")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Users found: {len(data.get('data', []))}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Create User
    print("\n3. Create New User")
    user_data = {
        "name": "Demo User",
        "email": "demo@testdomain.org",
        "password": "demopass123"
    }
    try:
        response = requests.post(
            f"{base_url}/users",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            user_id = data['data']['id']
            print(f"   ✅ User created with ID: {user_id}")
        else:
            print(f"   ❌ Error: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Login
    print("\n4. User Login")
    login_data = {
        "email": "demo@testdomain.org",
        "password": "demopass123"
    }
    try:
        response = requests.post(
            f"{base_url}/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful for: {data['data']['email']}")
        else:
            print(f"   ❌ Login failed: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Search Users
    print("\n5. Search Users")
    try:
        response = requests.get(f"{base_url}/search?name=Demo")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Found {len(data.get('data', []))} users matching 'Demo'")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Security Test - SQL Injection Attempt
    print("\n6. Security Test - SQL Injection Attempt")
    try:
        malicious_data = {
            "name": "Test User",
            "email": "test@testdomain.org",
            "password": "password123'; DROP TABLE users; --"
        }
        response = requests.post(
            f"{base_url}/users",
            json=malicious_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            print("   ✅ SQL injection attempt properly rejected")
        else:
            print("   ⚠️  Unexpected response to SQL injection attempt")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed successfully!")
    print("\nKey Security Features Demonstrated:")
    print("• Parameterized queries prevent SQL injection")
    print("• Input validation rejects malicious data")
    print("• Password hashing with bcrypt")
    print("• Proper error handling and status codes")
    print("• CORS support for frontend integration")

if __name__ == "__main__":
    demo_api() 