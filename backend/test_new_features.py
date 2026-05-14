"""
Quick Test Script for New AI-Optimized Features
Run this to verify the new endpoints are working
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/v1"

# You'll need to get a valid token first by logging in
# For now, this shows the endpoints that are available

print("=" * 60)
print("AI-OPTIMIZED FITNESS APP - ENDPOINT VERIFICATION")
print("=" * 60)
print()

# Test 1: Check if daily metrics endpoint exists
print("1. Testing Daily Metrics Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/daily-metrics/today")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✓ Endpoint exists (requires authentication)")
    elif response.status_code == 200:
        print("   ✓ Success!")
        print(f"   Data: {json.dumps(response.json(), indent=2)[:200]}...")
except Exception as e:
    print(f"   ✗ Error: {e}")
print()

# Test 2: Check nutrition analysis endpoint
print("2. Testing Nutrition Analysis Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/nutrition/analysis?days=7")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✓ Endpoint exists (requires authentication)")
    elif response.status_code == 200:
        print("   ✓ Success!")
except Exception as e:
    print(f"   ✗ Error: {e}")
print()

# Test 3: Check monthly nutrition stats
print("3. Testing Monthly Nutrition Stats...")
try:
    now = datetime.now()
    response = requests.get(f"{BASE_URL}/nutrition/monthly-stats?year={now.year}&month={now.month}")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✓ Endpoint exists (requires authentication)")
    elif response.status_code == 200:
        print("   ✓ Success!")
except Exception as e:
    print(f"   ✗ Error: {e}")
print()

# Test 4: Check AI insights endpoint
print("4. Testing AI Insights Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/daily-metrics/today/insights")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✓ Endpoint exists (requires authentication)")
    elif response.status_code == 200:
        print("   ✓ Success!")
except Exception as e:
    print(f"   ✗ Error: {e}")
print()

# Test 5: Check coach endpoint
print("5. Testing Enhanced Coach Endpoint...")
try:
    response = requests.post(f"{BASE_URL}/coach/chat?message=Hello")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✓ Endpoint exists (requires authentication)")
    elif response.status_code == 200:
        print("   ✓ Success!")
except Exception as e:
    print(f"   ✗ Error: {e}")
print()

print("=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
print()
print("Next Steps:")
print("1. Login to the app to get an authentication token")
print("2. Test the endpoints with a valid token")
print("3. Check the frontend integration")
print()
print("Frontend Features to Test:")
print("- Tap dashboard metrics to edit them")
print("- View AI insights on dashboard")
print("- Check nutrition monthly view")
print("- Test AI coach with context-aware responses")
