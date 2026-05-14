import requests
import json

# Test registration
print("Testing registration endpoint...")
response = requests.post(
    'http://localhost:8000/api/v1/users/',
    json={
        'email': 'testuser@example.com',
        'password': 'password123',
        'full_name': 'Test User',
        'is_active': True
    }
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code in [200, 201]:
    print("✓ Registration successful!")
else:
    print("✗ Registration failed")
