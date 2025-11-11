#!/usr/bin/env python3
"""
Simple HTTP Request Sender
Sends HTTP requests to specified URLs.
"""

import urllib.request
import urllib.error
import json
from typing import Optional, Dict, Any


class RequestSender:
    """A simple class to send HTTP requests."""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the RequestSender.
        
        Args:
            base_url: Optional base URL to prepend to all requests
        """
        self.base_url = base_url or ""
    
    def send_get_request(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Send a GET request to the specified URL.
        
        Args:
            url: The URL to send the request to
            headers: Optional dictionary of HTTP headers
            
        Returns:
            Dictionary containing response status, data, and headers
        """
        full_url = self.base_url + url if not url.startswith('http') else url
        
        try:
            req = urllib.request.Request(full_url, headers=headers or {})
            with urllib.request.urlopen(req) as response:
                data = response.read().decode('utf-8')
                return {
                    'status': response.status,
                    'data': data,
                    'headers': dict(response.headers)
                }
        except urllib.error.HTTPError as e:
            return {
                'status': e.code,
                'error': str(e),
                'data': None
            }
        except urllib.error.URLError as e:
            return {
                'status': 0,
                'error': str(e),
                'data': None
            }
    
    def send_post_request(self, url: str, data: Dict[str, Any], 
                         headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Send a POST request to the specified URL.
        
        Args:
            url: The URL to send the request to
            data: Dictionary of data to send in the request body
            headers: Optional dictionary of HTTP headers
            
        Returns:
            Dictionary containing response status, data, and headers
        """
        full_url = self.base_url + url if not url.startswith('http') else url
        
        # Prepare headers
        req_headers = headers or {}
        req_headers['Content-Type'] = 'application/json'
        
        # Encode data as JSON
        json_data = json.dumps(data).encode('utf-8')
        
        try:
            req = urllib.request.Request(full_url, data=json_data, headers=req_headers, method='POST')
            with urllib.request.urlopen(req) as response:
                response_data = response.read().decode('utf-8')
                return {
                    'status': response.status,
                    'data': response_data,
                    'headers': dict(response.headers)
                }
        except urllib.error.HTTPError as e:
            return {
                'status': e.code,
                'error': str(e),
                'data': None
            }
        except urllib.error.URLError as e:
            return {
                'status': 0,
                'error': str(e),
                'data': None
            }


def main():
    """Example usage of the RequestSender."""
    sender = RequestSender()
    
    # Example: Send a GET request
    print("Sending GET request to httpbin.org...")
    response = sender.send_get_request('https://httpbin.org/get')
    print(f"Status: {response['status']}")
    if response.get('data'):
        print(f"Response data: {response['data'][:200]}...")  # Print first 200 chars
    
    print("\n" + "="*50 + "\n")
    
    # Example: Send a POST request
    print("Sending POST request to httpbin.org...")
    post_data = {'message': 'Hello, World!', 'test': True}
    response = sender.send_post_request('https://httpbin.org/post', post_data)
    print(f"Status: {response['status']}")
    if response.get('data'):
        print(f"Response data: {response['data'][:200]}...")  # Print first 200 chars


if __name__ == '__main__':
    main()
