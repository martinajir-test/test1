"""
Sample web application demonstrating authorization handling with comprehensive 403 logging.
"""

import logging
from functools import wraps
from flask import Flask, request, jsonify
from datetime import datetime, timezone

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


def log_403_error(user_id, resource, required_permission, reason, extra_context=None):
    """
    Comprehensive logging function for 403 authorization errors.
    
    Args:
        user_id: The identifier of the user attempting the action
        resource: The resource/endpoint being accessed
        required_permission: The permission required for the action
        reason: Detailed reason for the authorization failure
        extra_context: Additional context information (dict)
    """
    log_data = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'error_type': '403_FORBIDDEN',
        'user_id': user_id,
        'resource': resource,
        'required_permission': required_permission,
        'reason': reason,
        'request_method': request.method,
        'request_path': request.path,
        'request_remote_addr': request.remote_addr,
        'request_user_agent': request.headers.get('User-Agent', 'Unknown'),
    }
    
    if extra_context:
        log_data['extra_context'] = extra_context
    
    # Log the 403 error with all relevant context
    logger.warning(
        f"403 AUTHORIZATION DENIED - User: {user_id}, Resource: {resource}, "
        f"Required: {required_permission}, Reason: {reason}, "
        f"IP: {request.remote_addr}, Path: {request.path}, Method: {request.method}"
    )
    
    # Also log as structured JSON for easier parsing
    logger.info(f"403_ERROR_DETAILS: {log_data}")


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
    app.run(debug=True, port=5000)
