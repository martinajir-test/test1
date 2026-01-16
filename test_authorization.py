"""
Tests for authorization logging functionality.
Validates that 403 errors are properly logged with relevant context.
"""

import unittest
import json
from io import StringIO
import logging
from app import app, log_403_error, USERS


class TestAuthorizationLogging(unittest.TestCase):
    """Test suite for 403 authorization error logging."""
    
    def setUp(self):
        """Set up test client and logging capture."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Capture log output
        self.log_capture = StringIO()
        self.handler = logging.StreamHandler(self.log_capture)
        self.handler.setLevel(logging.WARNING)
        logger = logging.getLogger('app')
        logger.addHandler(self.handler)
        logger.setLevel(logging.WARNING)
    
    def tearDown(self):
        """Clean up logging handlers."""
        logger = logging.getLogger('app')
        logger.removeHandler(self.handler)
    
    def get_log_output(self):
        """Get captured log output."""
        return self.log_capture.getvalue()
    
    def test_successful_authorization_read(self):
        """Test that authorized read request succeeds without 403 logging."""
        response = self.app.get('/api/data', headers={'X-User-ID': 'user1'})
        self.assertEqual(response.status_code, 200)
        
        # Should not log 403 error
        log_output = self.get_log_output()
        self.assertNotIn('403 AUTHORIZATION DENIED', log_output)
    
    def test_missing_user_id_logs_403(self):
        """Test that missing user ID triggers 403 with proper logging."""
        response = self.app.get('/api/data')
        self.assertEqual(response.status_code, 403)
        
        # Verify 403 is logged with context
        log_output = self.get_log_output()
        self.assertIn('403 AUTHORIZATION DENIED', log_output)
        self.assertIn('User: ANONYMOUS', log_output)
        self.assertIn('No user identification provided', log_output)
        self.assertIn('/api/data', log_output)
    
    def test_invalid_user_logs_403(self):
        """Test that invalid user triggers 403 with proper logging."""
        response = self.app.get('/api/data', headers={'X-User-ID': 'invalid_user'})
        self.assertEqual(response.status_code, 403)
        
        # Verify 403 is logged with user context
        log_output = self.get_log_output()
        self.assertIn('403 AUTHORIZATION DENIED', log_output)
        self.assertIn('User: invalid_user', log_output)
        self.assertIn('User not found in system', log_output)
    
    def test_insufficient_permissions_logs_403(self):
        """Test that insufficient permissions trigger 403 with detailed logging."""
        # user3 (guest) only has 'read' permission, try to write
        response = self.app.post('/api/data', headers={'X-User-ID': 'user3'})
        self.assertEqual(response.status_code, 403)
        
        # Verify 403 is logged with permission context
        log_output = self.get_log_output()
        self.assertIn('403 AUTHORIZATION DENIED', log_output)
        self.assertIn('User: user3', log_output)
        self.assertIn('Required: write', log_output)
        self.assertIn('User lacks required permission', log_output)
    
    def test_delete_without_permission_logs_403(self):
        """Test that delete without permission logs 403 with resource context."""
        # user2 doesn't have 'delete' permission
        response = self.app.delete('/api/data/123', headers={'X-User-ID': 'user2'})
        self.assertEqual(response.status_code, 403)
        
        # Verify 403 is logged with resource and permission details
        log_output = self.get_log_output()
        self.assertIn('403 AUTHORIZATION DENIED', log_output)
        self.assertIn('User: user2', log_output)
        self.assertIn('Required: delete', log_output)
    
    def test_admin_endpoint_logs_403_for_all_users(self):
        """Test that admin endpoint logs 403 for users without admin permission."""
        # None of the users have 'admin' permission
        response = self.app.get('/api/admin', headers={'X-User-ID': 'user1'})
        self.assertEqual(response.status_code, 403)
        
        # Verify 403 is logged
        log_output = self.get_log_output()
        self.assertIn('403 AUTHORIZATION DENIED', log_output)
        self.assertIn('User: user1', log_output)
        self.assertIn('/api/admin', log_output)
        self.assertIn('Required: admin', log_output)
    
    def test_log_includes_request_method(self):
        """Test that logged 403 includes HTTP request method."""
        response = self.app.post('/api/data', headers={'X-User-ID': 'user3'})
        self.assertEqual(response.status_code, 403)
        
        log_output = self.get_log_output()
        self.assertIn('Method: POST', log_output)
    
    def test_log_includes_request_path(self):
        """Test that logged 403 includes request path."""
        response = self.app.delete('/api/data/456', headers={'X-User-ID': 'user2'})
        self.assertEqual(response.status_code, 403)
        
        log_output = self.get_log_output()
        self.assertIn('Path: /api/data/456', log_output)
    
    def test_different_users_different_permissions(self):
        """Test that different users get appropriate 403s based on their permissions."""
        # user1 (admin) can delete - should succeed
        response = self.app.delete('/api/data/1', headers={'X-User-ID': 'user1'})
        self.assertEqual(response.status_code, 200)
        
        # user2 (user) cannot delete - should fail with 403
        response = self.app.delete('/api/data/2', headers={'X-User-ID': 'user2'})
        self.assertEqual(response.status_code, 403)
        
        log_output = self.get_log_output()
        # Should only log 403 for user2
        self.assertIn('User: user2', log_output)
        self.assertNotIn('User: user1', log_output)


class TestLogFunctionDirectly(unittest.TestCase):
    """Test the log_403_error function directly."""
    
    def setUp(self):
        """Set up logging capture."""
        self.log_capture = StringIO()
        self.handler = logging.StreamHandler(self.log_capture)
        self.handler.setLevel(logging.WARNING)
        logger = logging.getLogger('app')
        logger.addHandler(self.handler)
        logger.setLevel(logging.WARNING)
        
        # Create app context for request object
        self.app = app.test_client()
        self.ctx = app.test_request_context('/test/path', method='POST')
        self.ctx.push()
    
    def tearDown(self):
        """Clean up."""
        self.ctx.pop()
        logger = logging.getLogger('app')
        logger.removeHandler(self.handler)
    
    def test_log_403_includes_all_parameters(self):
        """Test that log_403_error function includes all provided parameters."""
        log_403_error(
            user_id='test_user',
            resource='/test/resource',
            required_permission='test_permission',
            reason='Test reason',
            extra_context={'key': 'value'}
        )
        
        log_output = self.log_capture.getvalue()
        self.assertIn('test_user', log_output)
        self.assertIn('/test/resource', log_output)
        self.assertIn('test_permission', log_output)
        self.assertIn('Test reason', log_output)


if __name__ == '__main__':
    unittest.main()
