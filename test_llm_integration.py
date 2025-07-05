#!/usr/bin/env python3
"""
Enhanced test script for LLM integration with error detection and solution suggestions
"""

import os
import sys
from dotenv import load_dotenv
from typing import Dict, List, Any, Tuple

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from src.llm_enhanced_analyzer import LLMEnhancedAnalyzer

class CodeValidationTester:
    """Enhanced tester that validates code correctness and provides solutions"""
    
    def __init__(self):
        self.analyzer = LLMEnhancedAnalyzer()
        
    def validate_code_correctness(self, code: str, language: str, expected_behavior: str = None, 
                                personality_type: str = None) -> Dict[str, Any]:
        """Validate if the code is correct and identify potential issues with personality-based insights"""
        
        # Get enhanced analysis with personality context
        if personality_type:
            analysis = self.analyzer.analyze_with_personality(code, language, personality_type)
        else:
            analysis = self.analyzer.analyze_code_with_llm(code, language)
        
        # Perform correctness validation
        validation_results = {
            'is_correct': True,
            'syntax_errors': [],
            'logic_errors': [],
            'runtime_errors': [],
            'performance_issues': [],
            'best_practice_violations': [],
            'solutions': [],
            'personality_type': personality_type
        }
        
        # Check for common issues based on traditional analysis
        validation_results.update(self._check_traditional_issues(analysis))
        
        # Get LLM-based correctness insights
        if self.analyzer.use_llm:
            llm_validation = self._get_llm_validation(code, language, expected_behavior, personality_type)
            validation_results.update(llm_validation)
        
        # Add personality-specific validation if available
        if personality_type and 'personality_insights' in analysis:
            validation_results['personality_insights'] = analysis['personality_insights']
        
        return validation_results
    
    def _check_traditional_issues(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Check for issues using traditional analysis"""
        issues = {
            'syntax_errors': [],
            'logic_errors': [],
            'performance_issues': []
        }
        
        # Check quality score
        quality_score = analysis.get('quality_score', 0)
        if quality_score < 5:
            issues['performance_issues'].append(f"Low quality score: {quality_score}")
        
        # Check complexity
        time_complexity = analysis.get('time_complexity', '')
        if 'O(n^2)' in time_complexity or 'O(n^3)' in time_complexity:
            issues['performance_issues'].append(f"High time complexity detected: {time_complexity}")
        
        return issues
    
    def _get_llm_validation(self, code: str, language: str, expected_behavior: str = None, 
                          personality_type: str = None) -> Dict[str, Any]:
        """Get LLM-based validation and error detection with personality context"""
        
        prompt = self._create_validation_prompt(code, language, expected_behavior, personality_type)
        
        try:
            response = self.analyzer.model.generate_content(
                prompt,
                generation_config=self.analyzer.model._generation_config or {}
            )
            return self._parse_validation_response(response.text)
        except Exception as e:
            print(f"LLM validation failed: {e}")
            return {}
    
    def _create_validation_prompt(self, code: str, language: str, expected_behavior: str = None, 
                                personality_type: str = None) -> str:
        """Create prompt for code validation with personality context"""
        
        behavior_context = f"\nExpected behavior: {expected_behavior}" if expected_behavior else ""
        
        personality_context = ""
        if personality_type and personality_type in self.analyzer.personality_types:
            personality_data = self.analyzer.personality_types[personality_type]
            personality_context = f"""
Student Personality Type: {personality_data['name']} ({personality_type})
Learning Style: {personality_data['learning_style']}
Focus Areas: {', '.join(personality_data['focus_areas'])}
Preferred Feedback: {personality_data['preferred_feedback']}

Please tailor your feedback and suggestions to match this personality type.
"""
        
        return f"""
You are an expert code reviewer and debugging specialist who provides personalized feedback.
Analyze the following {language} code for correctness, errors, and issues.

```{language}
{code}
```{behavior_context}

{personality_context}

Please provide a JSON response with detailed analysis:

{{
"is_correct": true/false,
"syntax_errors": ["list of syntax errors found"],
"logic_errors": ["list of logical errors or bugs"],
"runtime_errors": ["potential runtime errors"],
"performance_issues": ["performance problems identified"],
"best_practice_violations": ["code style/best practice issues"],
"correctness_explanation": "detailed explanation of why the code is correct/incorrect",
"error_locations": ["specific lines or sections with issues"],
"solutions": [
    {{
        "issue": "description of the issue",
        "solution": "how to fix it",
        "corrected_code": "fixed version of problematic code section",
        "explanation": "why this solution works",
        "personality_tip": "how this solution aligns with the student's personality type"
    }}
],
"test_cases": [
    {{
        "input": "test input",
        "expected_output": "expected result",
        "actual_behavior": "what the current code would produce"
    }}
],
"overall_assessment": "summary of code quality and correctness",
"personality_specific_feedback": "feedback tailored to the student's personality type and learning style"
}}
        """
    
    def _parse_validation_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM validation response"""
        try:
            import json
            
            # Clean response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Failed to parse validation response: {e}")
            return {
                'is_correct': False,
                'syntax_errors': [],
                'logic_errors': ['Failed to analyze code correctness'],
                'solutions': []
            }
    
    def generate_detailed_report(self, validation_results: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate a comprehensive report with errors and solutions"""
        
        report = []
        report.append("🔍 **CODE VALIDATION REPORT**")
        report.append("=" * 50)
        
        # Overall correctness
        is_correct = validation_results.get('is_correct', False)
        status_emoji = "✅" if is_correct else "❌"
        report.append(f"\n{status_emoji} **Overall Status:** {'CORRECT' if is_correct else 'ISSUES FOUND'}")
        
        if validation_results.get('correctness_explanation'):
            report.append(f"\n📝 **Analysis:** {validation_results['correctness_explanation']}")
        
        # Error sections
        error_sections = [
            ('syntax_errors', '🔴 **Syntax Errors:**'),
            ('logic_errors', '🟠 **Logic Errors:**'),
            ('runtime_errors', '🟡 **Runtime Errors:**'),
            ('performance_issues', '🔵 **Performance Issues:**'),
            ('best_practice_violations', '🟣 **Best Practice Violations:**')
        ]
        
        for error_type, title in error_sections:
            errors = validation_results.get(error_type, [])
            if errors:
                report.append(f"\n{title}")
                for error in errors:
                    report.append(f"   • {error}")
        
        # Solutions
        solutions = validation_results.get('solutions', [])
        if solutions:
            report.append("\n🛠️ **SOLUTIONS:**")
            for i, solution in enumerate(solutions, 1):
                report.append(f"\n   **Solution {i}:**")
                report.append(f"   Issue: {solution.get('issue', 'Unknown')}")
                report.append(f"   Fix: {solution.get('solution', 'No solution provided')}")
                if solution.get('corrected_code'):
                    report.append(f"   Corrected code: ```{solution['corrected_code']}```")
                if solution.get('explanation'):
                    report.append(f"   Why: {solution['explanation']}")
        
        # Test cases
        test_cases = validation_results.get('test_cases', [])
        if test_cases:
            report.append("\n🧪 **TEST CASES:**")
            for i, test in enumerate(test_cases, 1):
                report.append(f"\n   **Test {i}:**")
                report.append(f"   Input: {test.get('input', 'N/A')}")
                report.append(f"   Expected: {test.get('expected_output', 'N/A')}")
                report.append(f"   Actual: {test.get('actual_behavior', 'N/A')}")
        
        # Traditional analysis summary
        report.append("\n📊 **TECHNICAL ANALYSIS:**")
        report.append(f"   Time Complexity: {analysis.get('time_complexity', 'Unknown')}")
        report.append(f"   Space Complexity: {analysis.get('space_complexity', 'Unknown')}")
        report.append(f"   Quality Score: {analysis.get('quality_score', 0):.1f}/10")
        
        if validation_results.get('overall_assessment'):
            report.append(f"\n🎯 **OVERALL ASSESSMENT:**")
            report.append(f"   {validation_results['overall_assessment']}")
        
        return "\n".join(report)

def test_enhanced_llm_integration():
    """Test enhanced LLM integration with error detection and personality-based recommendations"""
    
    # Test cases with known issues and personality types
    test_cases = [
        {
            'name': 'Two Sum with Logic Error (Analytical Perspective)',
            'code': '''
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
''',
            'language': 'cpp',
            'expected_behavior': 'Find two numbers in array that add up to target and return their indices',
            'personality_type': 'analytical'
        },
        {
            'name': 'Correct Two Sum Implementation (Creative Perspective)',
            'code': '''
def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []
''',
            'language': 'python',
            'expected_behavior': 'Find two numbers in array that add up to target and return their indices',
            'personality_type': 'creative'
        },
        {
            'name': 'Practical Implementation with Error Handling',
            'code': '''
def two_sum(nums, target):
    if not nums or len(nums) < 2:
        return []
    
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []
''',
            'language': 'python',
            'expected_behavior': 'Find two numbers in array that add up to target and return their indices',
            'personality_type': 'practical'
        },
        {
            'name': 'Well-Documented Collaborative Solution',
            'code': '''
def two_sum(nums, target):
    """
    Find two numbers in the array that add up to target.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        List of two indices whose values add up to target
    """
    # Use hash map for O(1) lookup
    num_to_index = {}
    
    for current_index, current_num in enumerate(nums):
        # Calculate what number we need to find
        needed_num = target - current_num
        
        # Check if we've seen this number before
        if needed_num in num_to_index:
            return [num_to_index[needed_num], current_index]
        
        # Store current number and its index
        num_to_index[current_num] = current_index
    
    return []  # No solution found
''',
            'language': 'python',
            'expected_behavior': 'Find two numbers in array that add up to target and return their indices',
            'personality_type': 'collaborative'
        }
    ]
    
    print("🧪 **ENHANCED LLM INTEGRATION TEST**")
    print("=" * 60)
    
    tester = CodeValidationTester()
    
    print(f"✅ LLM Enabled: {tester.analyzer.use_llm}")
    if tester.analyzer.use_llm:
        print(f"✅ Gemini API Key configured: {bool(tester.analyzer.api_key)}")
    else:
        print("⚠️  Gemini API Key not found - using traditional analysis only")
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*20} TEST CASE {i}: {test_case['name']} {'='*20}")
        
        try:
            # Perform validation with personality context
            validation_results = tester.validate_code_correctness(
                test_case['code'], 
                test_case['language'], 
                test_case['expected_behavior'],
                test_case.get('personality_type')
            )
            
            # Get analysis with personality insights
            if test_case.get('personality_type'):
                analysis = tester.analyzer.analyze_with_personality(
                    test_case['code'], 
                    test_case['language'],
                    test_case['personality_type']
                )
            else:
                analysis = tester.analyzer.analyze_code_with_llm(
                    test_case['code'], 
                    test_case['language']
                )
            
            # Generate detailed report
            report = tester.generate_detailed_report(validation_results, analysis)
            print(report)
            
            # Show personality-specific insights if available
            if 'personality_insights' in validation_results:
                print(f"\n🎭 **PERSONALITY-SPECIFIC INSIGHTS:**")
                personality_summary = tester.analyzer.get_personality_summary(analysis)
                print(personality_summary)
            
            # Check if test passed
            if not validation_results.get('is_correct', False):
                print(f"\n⚠️  Test case {i} identified issues (as expected for buggy code)")
            else:
                print(f"\n✅ Test case {i} passed validation")
                
        except Exception as e:
            print(f"\n❌ Error in test case {i}: {e}")
            all_passed = False
    
    print(f"\n{'='*60}")
    print(f"🎯 **TEST SUMMARY:** {'All tests completed' if all_passed else 'Some tests failed'}")
    
    return all_passed

if __name__ == "__main__":
    success = test_enhanced_llm_integration()
    sys.exit(0 if success else 1)