#!/usr/bin/env python3
"""
Test script to verify Flask app endpoints work correctly
"""

import requests
import json
import time
from threading import Thread
from app import app

def start_test_server():
    """Start the Flask app in test mode"""
    app.run(debug=False, host='127.0.0.1', port=5001, use_reloader=False)

def test_endpoints():
    """Test the main endpoints"""
    base_url = "http://127.0.0.1:5001"
    
    # Wait for server to start
    time.sleep(2)
    
    print("🧪 Testing Flask App Endpoints")
    print("=" * 50)
    
    # Test 1: Home page
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Home page loads successfully")
        else:
            print(f"❌ Home page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Home page error: {e}")
    
    # Test 2: Code analysis endpoint
    try:
        test_code = """
def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []
"""
        
        payload = {
            "code": test_code,
            "language": "python",
            "problem_title": "Two Sum Test",
            "expected_behavior": "Find two numbers that add up to target"
        }
        
        response = requests.post(
            f"{base_url}/api/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'analysis' in data and 'recommendations' in data:
                print("✅ Code analysis endpoint works correctly")
                print(f"   Quality Score: {data['analysis'].get('quality_score', 'N/A')}")
                print(f"   Time Complexity: {data['analysis'].get('time_complexity', 'N/A')}")
            else:
                print("❌ Code analysis response missing expected fields")
        else:
            print(f"❌ Code analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Code analysis error: {e}")
    
    # Test 3: Code validation endpoint
    try:
        payload = {
            "code": test_code,
            "language": "python",
            "expected_behavior": "Find two numbers that add up to target"
        }
        
        response = requests.post(
            f"{base_url}/api/validate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'validation' in data:
                print("✅ Code validation endpoint works correctly")
                print(f"   Is Correct: {data['validation'].get('is_correct', 'N/A')}")
            else:
                print("❌ Code validation response missing expected fields")
        else:
            print(f"❌ Code validation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Code validation error: {e}")
    
    # Test 4: Resources endpoint
    try:
        response = requests.get(f"{base_url}/api/resources")
        if response.status_code == 200:
            data = response.json()
            if 'resources_by_concept' in data:
                print("✅ Resources endpoint works correctly")
            else:
                print("❌ Resources response missing expected fields")
        else:
            print(f"❌ Resources endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Resources endpoint error: {e}")
    
    print("\n🎯 **ENDPOINT TESTING COMPLETE**")

if __name__ == "__main__":
    # Start server in a separate thread
    server_thread = Thread(target=start_test_server, daemon=True)
    server_thread.start()
    
    # Run tests
    test_endpoints()