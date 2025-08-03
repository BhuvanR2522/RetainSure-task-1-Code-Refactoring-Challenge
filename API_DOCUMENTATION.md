# User Management API Documentation

## Live API Endpoints

The refactored User Management API is now deployed and available at:

**Production URL**: https://messy-migration-5maxrbes0-bhuvan-rs-projects-27d37f90.vercel.app

## API Endpoints

### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "success",
  "message": "User Management System is running"
}
```

### 2. Get All Users
```http
GET /users
```

**Response:**
```json
{
  "status": "success",
  "message": "Users retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2025-08-03T05:56:06",
      "updated_at": "2025-08-03T05:56:06"
    }
  ]
}
```

### 3. Get User by ID
```http
GET /user/{id}
```

**Response:**
```json
{
  "status": "success",
  "message": "User retrieved successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2025-08-03T05:56:06",
    "updated_at": "2025-08-03T05:56:06"
  }
}
```

### 4. Create User
```http
POST /users
Content-Type: application/json

{
  "name": "New User",
  "email": "newuser@example.com",
  "password": "securepass123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User created successfully",
  "data": {
    "id": 4,
    "name": "New User",
    "email": "newuser@example.com",
    "created_at": "2025-08-03T06:07:00"
  }
}
```

### 5. Update User
```http
PUT /user/{id}
Content-Type: application/json

{
  "name": "Updated User",
  "email": "updated@example.com"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User updated successfully",
  "data": {
    "id": 1,
    "name": "Updated User",
    "email": "updated@example.com",
    "created_at": "2025-08-03T05:56:06",
    "updated_at": "2025-08-03T06:07:00"
  }
}
```

### 6. Delete User
```http
DELETE /user/{id}
```

**Response:**
```json
{
  "status": "success",
  "message": "User deleted successfully"
}
```

### 7. Search Users
```http
GET /search?name={search_term}
```

**Response:**
```json
{
  "status": "success",
  "message": "Search completed successfully",
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2025-08-03T05:56:06",
      "updated_at": "2025-08-03T05:56:06"
    }
  ]
}
```

### 8. User Login
```http
POST /login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2025-08-03T05:56:06"
  }
}
```

## Error Responses

### Validation Error (400)
```json
{
  "status": "error",
  "error": "Email is required and must be a string"
}
```

### Not Found (404)
```json
{
  "status": "error",
  "error": "User not found"
}
```

### Conflict (409)
```json
{
  "status": "error",
  "error": "Email already exists"
}
```

### Unauthorized (401)
```json
{
  "status": "error",
  "error": "Invalid email or password"
}
```

## Security Features

✅ **SQL Injection Prevention**: All queries use parameterized statements
✅ **Password Hashing**: bcrypt with 12 salt rounds
✅ **Input Validation**: Comprehensive validation for all inputs
✅ **CORS Support**: Cross-origin requests enabled
✅ **Error Handling**: Proper HTTP status codes and error messages

## Testing the API

You can test the API using curl or any HTTP client:

```bash
# Health check
curl https://messy-migration-5maxrbes0-bhuvan-rs-projects-27d37f90.vercel.app/

# Get all users
curl https://messy-migration-5maxrbes0-bhuvan-rs-projects-27d37f90.vercel.app/users

# Create a user
curl -X POST https://messy-migration-5maxrbes0-bhuvan-rs-projects-27d37f90.vercel.app/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"testpass123"}'
```

## Repository

The complete source code is available at:
https://github.com/BhuvanR2522/RetainSure-task-1-Code-Refactoring-Challenge.git 