"""
Sample web application demonstrating authorization handling with comprehensive 403 logging.
"""

import logging
from functools import wraps
from flask import Flask, request, jsonify
from datetime import datetime, timezone
import json
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simulated user database
USERS = {
    'user1': {'role': 'admin', 'permissions': ['read', 'write', 'delete']},
    'user2': {'role': 'user', 'permissions': ['read', 'write']},
    'user3': {'role': 'guest', 'permissions': ['read']},
}


def sanitize_for_logging(value, max_length=1000):
    """
    Sanitize user-provided values to prevent log injection attacks.
    
    Args:
        value: The value to sanitize
        max_length: Maximum allowed length for the value
    
    Returns:
        Sanitized string safe for logging
    """
    if value is None:
        return 'None'
    
    # Convert to string
    str_value = str(value)
    
    # Truncate if too long to prevent log flooding
    if len(str_value) > max_length:
        str_value = str_value[:max_length] + '...[truncated]'
    
    # Remove or escape newlines and carriage returns to prevent log injection
    str_value = str_value.replace('\n', '\\n').replace('\r', '\\r')
    
    # Remove other control characters except tab
    str_value = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', str_value)
    
    return str_value


def log_403_error(user_id, resource, required_permission, reason, extra_context=None):
    """
    Comprehensive logging function for 403 authorization errors.
    Uses sanitization to prevent log injection attacks.
    
    Args:
        user_id: The identifier of the user attempting the action
        resource: The resource/endpoint being accessed
        required_permission: The permission required for the action
        reason: Detailed reason for the authorization failure
        extra_context: Additional context information (dict)
    """
    # Sanitize all user-provided inputs
    safe_user_id = sanitize_for_logging(user_id, max_length=100)
    safe_resource = sanitize_for_logging(resource, max_length=200)
    safe_permission = sanitize_for_logging(required_permission, max_length=100)
    safe_reason = sanitize_for_logging(reason, max_length=500)
    
    log_data = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'error_type': '403_FORBIDDEN',
        'user_id': safe_user_id,
        'resource': safe_resource,
        'required_permission': safe_permission,
        'reason': safe_reason,
        'request_method': sanitize_for_logging(request.method, max_length=10),
        'request_path': sanitize_for_logging(request.path, max_length=500),
        'request_remote_addr': sanitize_for_logging(request.remote_addr, max_length=50),
        'request_user_agent': sanitize_for_logging(
            request.headers.get('User-Agent', 'Unknown'), 
            max_length=200
        ),
    }
    
    if extra_context:
        # Sanitize extra context by converting to JSON and back
        # This ensures it's safe and properly structured
        try:
            safe_extra_context = json.loads(json.dumps(extra_context))
            log_data['extra_context'] = safe_extra_context
        except (TypeError, ValueError):
            log_data['extra_context'] = {'error': 'Could not serialize extra_context'}
    
    # Log the 403 error with all relevant context (using sanitized values)
    logger.warning(
        f"403 AUTHORIZATION DENIED - User: {safe_user_id}, Resource: {safe_resource}, "
        f"Required: {safe_permission}, Reason: {safe_reason}, "
        f"IP: {log_data['request_remote_addr']}, "
        f"Path: {log_data['request_path']}, Method: {log_data['request_method']}"
    )
    
    # Log as structured JSON (already sanitized)
    logger.info(f"403_ERROR_DETAILS: {json.dumps(log_data)}")



def require_permission(permission):
    """
    Decorator to check if user has required permission.
    Logs detailed information when authorization fails (403).
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get user from request (in real app, this would come from token/session)
            user_id = request.headers.get('X-User-ID')
            
            if not user_id:
                # Log missing authentication
                log_403_error(
                    user_id='ANONYMOUS',
                    resource=request.endpoint or request.path,
                    required_permission=permission,
                    reason='No user identification provided',
                    extra_context={'headers': dict(request.headers)}
                )
                return jsonify({'error': 'Forbidden', 'message': 'Authentication required'}), 403
            
            user = USERS.get(user_id)
            
            if not user:
                # Log unknown user
                log_403_error(
                    user_id=user_id,
                    resource=request.endpoint or request.path,
                    required_permission=permission,
                    reason=f'User not found in system',
                    extra_context={'attempted_user_id': user_id}
                )
                return jsonify({'error': 'Forbidden', 'message': 'Invalid user'}), 403
            
            if permission not in user['permissions']:
                # Log insufficient permissions
                log_403_error(
                    user_id=user_id,
                    resource=request.endpoint or request.path,
                    required_permission=permission,
                    reason=f'User lacks required permission. Has: {user["permissions"]}, Needs: {permission}',
                    extra_context={
                        'user_role': user['role'],
                        'user_permissions': user['permissions']
                    }
                )
                return jsonify({
                    'error': 'Forbidden',
                    'message': f'Insufficient permissions. Required: {permission}'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/api/data', methods=['GET'])
@require_permission('read')
def get_data():
    """Endpoint that requires read permission."""
    logger.info("Successfully accessed /api/data")
    return jsonify({'data': 'Sample data', 'message': 'Read successful'})


@app.route('/api/data', methods=['POST'])
@require_permission('write')
def create_data():
    """Endpoint that requires write permission."""
    logger.info("Successfully accessed POST /api/data")
    return jsonify({'message': 'Data created successfully'})


@app.route('/api/data/<int:data_id>', methods=['DELETE'])
@require_permission('delete')
def delete_data(data_id):
    """Endpoint that requires delete permission."""
    logger.info(f"Successfully deleted data with ID: {data_id}")
    return jsonify({'message': f'Data {data_id} deleted successfully'})


@app.route('/api/admin', methods=['GET'])
@require_permission('admin')
def admin_endpoint():
    """Endpoint that requires admin permission (which no user has)."""
    logger.info("Successfully accessed /api/admin")
    return jsonify({'message': 'Admin access granted'})


@app.errorhandler(403)
def handle_403(e):
    """
    Global 403 error handler to catch any 403 errors not handled by decorators.
    """
    log_403_error(
        user_id=request.headers.get('X-User-ID', 'UNKNOWN'),
        resource=request.path,
        required_permission='UNKNOWN',
        reason='Generic 403 error - not caught by specific handler',
        extra_context={'error': str(e)}
    )
    return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403


if __name__ == '__main__':
    # Note: debug=True is for development/demonstration only
    # In production, set debug=False and use a production WSGI server
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode, port=5000)

