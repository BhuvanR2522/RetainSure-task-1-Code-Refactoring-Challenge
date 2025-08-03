# User Management API

A secure, refactored user management API built with Flask and SQLite.

## Features

- ✅ Secure password hashing with bcrypt
- ✅ SQL injection prevention with parameterized queries
- ✅ Comprehensive input validation and sanitization
- ✅ Proper error handling and HTTP status codes
- ✅ CORS support for frontend integration
- ✅ Environment-based configuration
- ✅ Comprehensive test suite
- ✅ Production-ready security features

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd messy-migration
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python init_db.py
   ```

4. Start the application:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/users` | Get all users |
| GET | `/user/<id>` | Get specific user |
| POST | `/users` | Create new user |
| PUT | `/user/<id>` | Update user |
| DELETE | `/user/<id>` | Delete user |
| GET | `/search?name=<name>` | Search users by name |
| POST | `/login` | User login |

## Example Usage

### Create a User
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### Get All Users
```bash
curl http://localhost:5000/users
```

## Testing

Run the test suite:
```bash
pytest test_app.py
```

## Configuration

Create a `.env` file for custom configuration:

```env
SECRET_KEY=your-secure-secret-key
DEBUG=False
HOST=127.0.0.1
PORT=5000
DATABASE_PATH=users.db
```

## Security Features

- **Password Hashing**: All passwords are hashed using bcrypt
- **SQL Injection Prevention**: Parameterized queries prevent SQL injection
- **Input Validation**: Comprehensive validation for all inputs
- **Data Sanitization**: Input sanitization prevents XSS attacks
- **Environment Configuration**: Secure configuration management

## Project Structure

```
messy-migration/
├── app.py              # Main Flask application
├── config.py           # Configuration management
├── database.py         # Database operations
├── validators.py       # Input validation
├── init_db.py          # Database initialization
├── test_app.py         # Test suite
├── requirements.txt    # Dependencies
├── CHANGES.md         # Refactoring documentation
└── README.md          # This file
```

## Development

### Running in Development Mode
```bash
export DEBUG=True
python app.py
```

### Database Reset
```bash
rm users.db
python init_db.py
```

## Security Checklist

- ✅ SQL Injection Prevention
- ✅ Password Hashing (bcrypt)
- ✅ Input Validation and Sanitization
- ✅ Environment-Based Configuration
- ✅ Proper Error Handling
- ✅ CORS Support
- ✅ Request Content-Type Validation
- ✅ Email Format Validation
- ✅ Password Strength Requirements
- ✅ Data Sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is for educational purposes.

## Support

For issues and questions, please refer to the `CHANGES.md` file for detailed documentation of the refactoring process.