import requests
import json

# Test registration endpoint
url = "http://localhost:8000/api/register/"
data = {
    "username": "testuser123",
    "email": "test123@example.com",
    "password": "testpass123",
    "role": "viewer"
}

print("Testing registration endpoint...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(url, json=data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"\nError: {e}")
    print(f"Response text: {response.text if 'response' in locals() else 'No response'}")

# Test login endpoint
print("\n" + "="*50)
print("Testing login endpoint...")
login_url = "http://localhost:8000/api/token/"
login_data = {
    "username": "testuser123",
    "password": "testpass123"
}

try:
    response = requests.post(login_url, json=login_data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"\nError: {e}")
    print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
