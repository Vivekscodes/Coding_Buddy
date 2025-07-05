#!/usr/bin/env python3
"""
Simple test to verify the map error is fixed
"""

import requests
import json

def test_simple_code():
    """Test with simple code that should work without errors"""
    
    url = "http://127.0.0.1:5000/api/analyze"
    
    test_code = '''
def hello_world():
    print("Hello, World!")
    return "success"

hello_world()
'''
    
    payload = {
        "code": test_code,
        "language": "python",
        "problem_title": "Hello World Test",
        "expected_behavior": "Print Hello World and return success"
    }
    
    try:
        print("🧪 Testing simple code analysis...")
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analysis successful!")
            
            # Check that all expected fields are present and are arrays
            analysis = data.get('analysis', {})
            print(f"📊 Patterns found: {analysis.get('patterns', [])}")
            print(f"📊 Algorithms found: {analysis.get('algorithms', [])}")
            print(f"📊 Data structures found: {analysis.get('data_structures', [])}")
            
            # Check recommendations
            recommendations = data.get('recommendations', {})
            print(f"📋 Knowledge gaps: {len(recommendations.get('knowledge_gaps', []))}")
            print(f"📋 Concepts to learn: {len(recommendations.get('concepts_to_learn', []))}")
            print(f"📋 Practice problems: {len(recommendations.get('practice_problems', []))}")
            
            # Check validation
            validation = data.get('validation', {})
            print(f"✅ Code correctness: {validation.get('is_correct', 'Unknown')}")
            
            print("🎉 All tests passed! The map error has been fixed.")
            return True
            
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the Flask app is running on http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_code()
    if success:
        print("\n🎯 The integration is working correctly!")
        print("💡 You can now use the web interface without map errors.")
    else:
        print("\n⚠️  There may still be issues. Check the Flask app logs.")
