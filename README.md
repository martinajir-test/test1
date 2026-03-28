test
# Update made by branch feature-branch-8

test


mergeable


test
asdfasf

## HTTP Request Sender

This repository includes a simple HTTP request sender utility for making GET and POST requests.

### Usage

The `request_sender.py` module provides a `RequestSender` class for sending HTTP requests:

```python
from request_sender import RequestSender

# Create a sender instance
sender = RequestSender()

# Send a GET request
response = sender.send_get_request('https://api.example.com/data')
print(f"Status: {response['status']}")
print(f"Data: {response['data']}")

# Send a POST request
data = {'key': 'value'}
response = sender.send_post_request('https://api.example.com/create', data)
print(f"Status: {response['status']}")
```

You can also initialize with a base URL:

```python
sender = RequestSender(base_url='https://api.example.com')
response = sender.send_get_request('/endpoint')  # Will request https://api.example.com/endpoint
```

### Running the Example

Run the example script to see it in action:

```bash
python3 request_sender.py
```

### Running Tests

Run the test suite:

```bash
python3 -m unittest test_request_sender.py
```
