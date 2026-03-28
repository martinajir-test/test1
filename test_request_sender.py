#!/usr/bin/env python3
"""
Tests for the request_sender module.
"""

import unittest
from unittest.mock import patch, Mock
from request_sender import RequestSender
import urllib.error


class TestRequestSender(unittest.TestCase):
    """Test cases for RequestSender class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sender = RequestSender()
        self.sender_with_base = RequestSender(base_url="https://api.example.com")
    
    @patch('urllib.request.urlopen')
    def test_send_get_request_success(self, mock_urlopen):
        """Test successful GET request."""
        # Mock response
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"result": "success"}'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)
        mock_urlopen.return_value = mock_response
        
        result = self.sender.send_get_request('https://example.com/api')
        
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['data'], '{"result": "success"}')
        self.assertIn('Content-Type', result['headers'])
    
    @patch('urllib.request.urlopen')
    def test_send_get_request_http_error(self, mock_urlopen):
        """Test GET request with HTTP error."""
        mock_urlopen.side_effect = urllib.error.HTTPError(
            'https://example.com/api', 404, 'Not Found', {}, None
        )
        
        result = self.sender.send_get_request('https://example.com/api')
        
        self.assertEqual(result['status'], 404)
        self.assertIn('error', result)
        self.assertIsNone(result['data'])
    
    @patch('urllib.request.urlopen')
    def test_send_post_request_success(self, mock_urlopen):
        """Test successful POST request."""
        # Mock response
        mock_response = Mock()
        mock_response.status = 201
        mock_response.read.return_value = b'{"created": true}'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)
        mock_urlopen.return_value = mock_response
        
        data = {'key': 'value'}
        result = self.sender.send_post_request('https://example.com/api', data)
        
        self.assertEqual(result['status'], 201)
        self.assertEqual(result['data'], '{"created": true}')
    
    def test_base_url_initialization(self):
        """Test RequestSender with base URL."""
        self.assertEqual(self.sender_with_base.base_url, "https://api.example.com")
    
    @patch('urllib.request.urlopen')
    def test_base_url_prepending(self, mock_urlopen):
        """Test that base URL is prepended to relative URLs."""
        mock_response = Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"result": "ok"}'
        mock_response.headers = {}
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)
        mock_urlopen.return_value = mock_response
        
        # Relative URL should have base prepended
        result = self.sender_with_base.send_get_request('/endpoint')
        self.assertEqual(result['status'], 200)
        
        # Absolute URL should not have base prepended
        result = self.sender_with_base.send_get_request('https://other.com/endpoint')
        self.assertEqual(result['status'], 200)


if __name__ == '__main__':
    unittest.main()
