import requests
import random

email = f'finaltest{random.randint(1000,9999)}@test.com'
response = requests.post(
    'http://localhost:8000/api/v1/users/',
    json={
        'email': email,
        'password': 'password123',
        'full_name': 'Final Test User'
    }
)

print(f'Email: {email}')
print(f'Status: {response.status_code}')

if response.status_code == 200 or response.status_code == 201:
    print('✓ SUCCESS! Registration works!')
    print(f'User data: {response.json()}')
else:
    print(f'✗ Error: {response.text[:300]}')
