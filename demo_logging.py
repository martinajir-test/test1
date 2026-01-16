#!/usr/bin/env python3
"""
Demonstration script showing 403 authorization logging in action.
This script makes various API calls to trigger different authorization scenarios.
"""

import requests
import time
import sys

BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print('=' * 70)

def make_request(method, endpoint, user_id=None, description=""):
    """Make a request and display the result."""
    headers = {}
    if user_id:
        headers['X-User-ID'] = user_id
    
    print(f"\n{description}")
    print(f"  Request: {method} {endpoint}")
    print(f"  User: {user_id or 'NONE (anonymous)'}")
    
    try:
        if method == 'GET':
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        elif method == 'POST':
            response = requests.post(f"{BASE_URL}{endpoint}", headers=headers)
        elif method == 'DELETE':
            response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
        
        print(f"  Response: {response.status_code}")
        print(f"  Body: {response.json()}")
        
        if response.status_code == 403:
            print("  ⚠️  403 FORBIDDEN - Check server logs for detailed authorization failure info")
        elif response.status_code == 200:
            print("  ✅ SUCCESS")
        
    except requests.exceptions.ConnectionError:
        print("  ❌ ERROR: Cannot connect to server. Make sure the Flask app is running:")
        print("     python app.py")
        sys.exit(1)

def main():
    """Run demonstration scenarios."""
    print("\n" + "=" * 70)
    print("  403 AUTHORIZATION LOGGING DEMONSTRATION")
    print("=" * 70)
    print("\nThis script demonstrates the comprehensive logging that occurs")
    print("when 403 authorization errors happen in the application.")
    print("\nWatch the Flask server logs to see detailed 403 error information!")
    
    time.sleep(2)
    
    # Scenario 1: Missing authentication
    print_section("Scenario 1: Missing Authentication")
    make_request('GET', '/api/data', None,
                 "Attempting to access data without user ID")
    
    time.sleep(1)
    
    # Scenario 2: Invalid user
    print_section("Scenario 2: Invalid/Unknown User")
    make_request('GET', '/api/data', 'hacker123',
                 "Attempting to access data with invalid user ID")
    
    time.sleep(1)
    
    # Scenario 3: Insufficient permissions (write)
    print_section("Scenario 3: Insufficient Permissions (Write)")
    make_request('POST', '/api/data', 'user3',
                 "Guest user (read-only) attempting to write data")
    
    time.sleep(1)
    
    # Scenario 4: Insufficient permissions (delete)
    print_section("Scenario 4: Insufficient Permissions (Delete)")
    make_request('DELETE', '/api/data/456', 'user2',
                 "Regular user attempting to delete data (needs admin)")
    
    time.sleep(1)
    
    # Scenario 5: Permission not defined
    print_section("Scenario 5: Permission Not Defined")
    make_request('GET', '/api/admin', 'user1',
                 "Admin user attempting to access endpoint requiring 'admin' permission")
    
    time.sleep(1)
    
    # Scenario 6: Successful access
    print_section("Scenario 6: Successful Authorization")
    make_request('GET', '/api/data', 'user1',
                 "Admin user with read permission accessing data")
    
    time.sleep(1)
    
    print_section("Demonstration Complete")
    print("\nCheck the Flask server logs to see:")
    print("  • Detailed 403 authorization denial messages")
    print("  • User information and their permissions")
    print("  • Required vs actual permissions")
    print("  • Request details (method, path, IP, user-agent)")
    print("  • Structured JSON log entries with full context")
    print("\nExample log entry format:")
    print("  2026-01-16 14:30:15 - WARNING - 403 AUTHORIZATION DENIED")
    print("    User: user3, Resource: create_data, Required: write,")
    print("    Reason: User lacks required permission. Has: ['read'], Needs: write")
    print("    IP: 127.0.0.1, Path: /api/data, Method: POST")
    print()

if __name__ == '__main__':
    main()
