# 403 Authorization Logging

Simple example of adding logging when 403 authorization errors occur.

## What it does

The `auth_example.py` script shows how to log authorization failures:
- Logs when unknown users try to access resources
- Logs when users lack required permissions
- Includes user info and permission details in logs

## Usage

```bash
python auth_example.py
```

## Example Output

```
WARNING:__main__:403 - User 'guest' lacks 'write' permission. Has: ['read']
WARNING:__main__:403 - Unknown user 'hacker' attempted access
```

## Adding to Your Code

To add 403 logging to your application:

1. Use `logger.warning()` when returning a 403 error
2. Include relevant context: user, resource, required permission
3. Log the reason for denial

Example:
```python
logger.warning(f"403 - User '{user_id}' lacks '{permission}' permission")
```
