# Authorization Logging Implementation

## Overview

This repository demonstrates comprehensive logging for 403 authorization errors in a web application. The implementation captures detailed context whenever a 403 Forbidden error occurs, making it easier to debug authorization issues.

## Features

### 1. Comprehensive 403 Error Logging

When a 403 authorization error occurs, the system logs:

- **Timestamp**: When the error occurred (UTC)
- **User Information**: User ID attempting the action
- **Resource**: The endpoint/resource being accessed
- **Required Permission**: What permission was needed
- **User's Actual Permissions**: What permissions the user has
- **User Role**: The role of the user
- **Request Details**:
  - HTTP method (GET, POST, DELETE, etc.)
  - Request path
  - Remote IP address
  - User-Agent string
- **Failure Reason**: Detailed explanation of why authorization failed
- **Extra Context**: Any additional relevant information

### 2. Authorization Decorator

The `@require_permission()` decorator provides:
- Easy permission checking for endpoints
- Automatic 403 logging on authorization failure
- Clean separation of authorization logic from business logic

### 3. Multiple Authorization Scenarios

The implementation handles and logs:
- Missing authentication (no user ID provided)
- Invalid/unknown users
- Insufficient permissions
- Missing specific permissions

## Files

- **app.py**: Main Flask application with authorization middleware and logging
- **test_authorization.py**: Comprehensive test suite validating logging behavior
- **demo_logging.py**: Interactive demonstration script showing logging in action
- **requirements.txt**: Python dependencies
- **AUTHORIZATION_LOGGING.md**: This documentation file

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python app.py
```

The server starts on `http://localhost:5000`.

### Testing Authorization

Use the `X-User-ID` header to simulate different users:

```bash
# Successful request (user1 has read permission)
curl -H "X-User-ID: user1" http://localhost:5000/api/data

# 403 - Missing authentication
curl http://localhost:5000/api/data

# 403 - Invalid user
curl -H "X-User-ID: invalid_user" http://localhost:5000/api/data

# 403 - Insufficient permissions (user3 only has read, trying to write)
curl -X POST -H "X-User-ID: user3" http://localhost:5000/api/data

# 403 - No delete permission (user2 cannot delete)
curl -X DELETE -H "X-User-ID: user2" http://localhost:5000/api/data/123
```

### Example Log Output

When a 403 error occurs, you'll see detailed logs like:

```
2026-01-16 14:30:15,123 - app - WARNING - 403 AUTHORIZATION DENIED - User: user3, Resource: create_data, Required: write, Reason: User lacks required permission. Has: ['read'], Needs: write, IP: 127.0.0.1, Path: /api/data, Method: POST

2026-01-16 14:30:15,124 - app - INFO - 403_ERROR_DETAILS: {'timestamp': '2026-01-16T14:30:15.123456', 'error_type': '403_FORBIDDEN', 'user_id': 'user3', 'resource': 'create_data', 'required_permission': 'write', 'reason': "User lacks required permission. Has: ['read'], Needs: write", 'request_method': 'POST', 'request_path': '/api/data', 'request_remote_addr': '127.0.0.1', 'request_user_agent': 'curl/7.68.0', 'extra_context': {'user_role': 'guest', 'user_permissions': ['read']}}
```

## Running Tests

```bash
python -m pytest test_authorization.py -v
```

Or with unittest:

```bash
python test_authorization.py
```

## Interactive Demonstration

To see the 403 logging in action with various scenarios:

1. Start the Flask application in one terminal:
```bash
python app.py
```

2. In another terminal, run the demo script:
```bash
python demo_logging.py
```

The demo script will trigger various 403 scenarios and show you the responses. Watch the Flask app's terminal output to see the detailed logging for each 403 error.

## User Permissions

The application includes three simulated users with different permission levels:

| User ID | Role  | Permissions           |
|---------|-------|-----------------------|
| user1   | admin | read, write, delete   |
| user2   | user  | read, write           |
| user3   | guest | read                  |

## Logging Architecture

### Log Levels

- **WARNING**: Human-readable 403 authorization denials
- **INFO**: Structured JSON log entries with full context

### Log Function: `log_403_error()`

The central logging function that captures:
- All required context about the authorization failure
- Request metadata (IP, User-Agent, method, path)
- User information and permissions
- Detailed failure reason
- Optional extra context

### Authorization Decorator: `@require_permission()`

Wraps endpoints to:
1. Check if user is authenticated
2. Verify user exists in the system
3. Validate user has required permission
4. Log detailed 403 information if any check fails
5. Return appropriate error response

### Global Error Handler: `@app.errorhandler(403)`

Catches any 403 errors not handled by specific decorators and ensures they're logged.

## Benefits

1. **Better Debugging**: Detailed context helps identify authorization issues quickly
2. **Security Monitoring**: Track unauthorized access attempts
3. **User Support**: Understand why users are getting denied access
4. **Audit Trail**: Complete record of authorization failures
5. **Compliance**: Detailed logs for security audits

## Extending the Implementation

To add logging to your own application:

1. Copy the `log_403_error()` function
2. Use the `@require_permission()` decorator pattern
3. Ensure all 403 responses call the logging function
4. Add any application-specific context to `extra_context`

## Security Considerations

### Log Injection Prevention
This implementation includes **built-in sanitization** to prevent log injection attacks:
- **Newlines and carriage returns** are escaped (`\n`, `\r`) to prevent fake log entries
- **Control characters** are removed to prevent terminal manipulation
- **Input length** is limited (1000 chars default) to prevent log flooding
- **Extra context** is validated as proper JSON to prevent injection
- All user-provided inputs are sanitized before logging

### Best Practices
- Logs include sensitive information (user IDs, IPs) - **secure your log files**
- Implement proper **log file permissions** (e.g., 600 or 640)
- Use **log rotation** to manage log file sizes
- Consider **log retention policies** based on compliance needs
- Review logs regularly for **security incidents**
- Comply with **privacy regulations** (GDPR, CCPA, etc.)

### What NOT to Log
- ❌ Passwords or authentication tokens
- ❌ Credit card numbers or PII
- ❌ Session tokens or API keys
- ❌ Full request bodies with sensitive data
- ✅ Only metadata needed for debugging authorization
