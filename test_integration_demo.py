#!/usr/bin/env python3
"""
Demo script to test the integrated LLM validation system
"""

import requests
import json

# Test the new validation endpoint
def test_validation_endpoint():
    url = "http://127.0.0.1:5000/api/validate"
    
    # Test case with a buggy Two Sum implementation
    test_code = '''
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        int res=0;
        unordered_map<int,int> ans;
        
       for(int i=0; i<nums.size(); i++){
        res=abs(target-nums[i]);  // BUG: should be target-nums[i], not abs()
        if(ans.count(res)){
            return {ans[res],i};
        }
        ans[nums[i]]=i;
       }
       return {};
    }
};
'''
    
    payload = {
        "code": test_code,
        "language": "cpp",
        "expected_behavior": "Find two numbers in array that add up to target and return their indices"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            validation = data.get('validation', {})
            print("✅ Validation endpoint working!")
            print(f"Code is correct: {validation.get('is_correct', False)}")
            syntax_errors = validation.get('syntax_errors', [])
            logic_errors = validation.get('logic_errors', [])
            print(f"Syntax errors: {len(syntax_errors)}")
            print(f"Logic errors: {len(logic_errors)}")
            print(f"Solutions provided: {len(validation.get('solutions', []))}")
            if logic_errors:
                print(f"Sample logic error: {logic_errors[0][:100]}...")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect: Is the Flask app running on http://127.0.0.1:5000?")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")

# Test the enhanced analyze endpoint
def test_analyze_endpoint():
    url = "http://127.0.0.1:5000/api/analyze"
    
    # Test case with correct code
    test_code = '''
def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []
'''
    
    payload = {
        "code": test_code,
        "language": "python",
        "problem_title": "Two Sum",
        "expected_behavior": "Find two numbers in array that add up to target and return their indices"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Enhanced analyze endpoint working!")
            print(f"Analysis available: {'analysis' in data}")
            print(f"Recommendations available: {'recommendations' in data}")
            print(f"Validation available: {'validation' in data}")
            print(f"Detailed report available: {'detailed_report' in data}")
            
            if 'validation' in data:
                validation = data['validation']
                print(f"Code correctness: {validation.get('is_correct', 'Unknown')}")
                print(f"LLM assessment: {validation.get('overall_assessment', 'No assessment')[:100]}...")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect: Is the Flask app running on http://127.0.0.1:5000?")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")

if __name__ == "__main__":
    print("🧪 Testing LLM Integration...")
    print("=" * 50)
    
    print("\n1. Testing validation endpoint:")
    test_validation_endpoint()
    
    print("\n2. Testing enhanced analyze endpoint:")
    test_analyze_endpoint()
    
    print("\n🎯 Test completed!")
    print("\nYou can now open http://127.0.0.1:5000 in your browser to test the frontend!")
