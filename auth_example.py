"""
Simple example showing 403 authorization logging.
"""
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_authorization(user_id, required_permission):
    """
    Check if user has permission. Logs when 403 occurs.
    """
    # Simple user permissions database
    users = {
        'admin': ['read', 'write', 'delete'],
        'user': ['read', 'write'],
        'guest': ['read']
    }
    
    user_perms = users.get(user_id)
    
    if not user_perms:
        # Log 403 - unknown user
        logger.warning(f"403 - Unknown user '{user_id}' attempted access")
        return False
    
    if required_permission not in user_perms:
        # Log 403 - insufficient permissions
        logger.warning(
            f"403 - User '{user_id}' lacks '{required_permission}' permission. "
            f"Has: {user_perms}"
        )
        return False
    
    return True

# Example usage
if __name__ == '__main__':
    print("Testing authorization with logging:\n")
    
    # Test 1: Valid user with permission
    print("1. Admin user reading data:")
    if check_authorization('admin', 'read'):
        print("   ✓ Access granted\n")
    else:
        print("   ✗ Access denied\n")
    
    # Test 2: Valid user without permission
    print("2. Guest user trying to write:")
    if check_authorization('guest', 'write'):
        print("   ✓ Access granted\n")
    else:
        print("   ✗ Access denied (check logs for details)\n")
    
    # Test 3: Unknown user
    print("3. Unknown user trying to read:")
    if check_authorization('hacker', 'read'):
        print("   ✓ Access granted\n")
    else:
        print("   ✗ Access denied (check logs for details)\n")
