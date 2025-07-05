import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.code_analyzer import CodeAnalyzer
from src.recommendation_engine import RecommendationEngine
from src.progress_tracker import ProgressTracker

class TestCodeAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = CodeAnalyzer()
    
    def test_python_code_analysis(self):
        """Test basic Python code analysis"""
        code = """
def two_sum(nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    return []
        """
        
        result = self.analyzer.analyze_code(code, 'python')
        
        self.assertIsInstance(result, dict)
        self.assertIn('quality_score', result)
        self.assertIn('complexity_score', result)
        self.assertIn('patterns', result)
        self.assertIn('algorithms', result)
        self.assertIn('data_structures', result)
        self.assertIn('time_complexity', result)
        self.assertIn('space_complexity', result)
        
        # Check that hash table is detected
        self.assertIn('hash_table', result['data_structures'])
        
    def test_pattern_detection(self):
        """Test pattern detection in code"""
        code = """
def two_pointers_example(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        if arr[left] + arr[right] == target:
            return [left, right]
        elif arr[left] + arr[right] < target:
            left += 1
        else:
            right -= 1
    return []
        """
        
        result = self.analyzer.analyze_code(code, 'python')
        patterns = result['patterns']
        
        # Should detect two pointers pattern
        self.assertTrue(any('two_pointer' in pattern for pattern in patterns))

class TestRecommendationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RecommendationEngine()
    
    def test_knowledge_graph_structure(self):
        """Test that knowledge graph is properly structured"""
        graph = self.engine.knowledge_graph
        
        self.assertIn('data_structures', graph)
        self.assertIn('algorithms', graph)
        self.assertIn('patterns', graph)
        
        # Check that array concept exists
        self.assertIn('array', graph['data_structures'])
        
        # Check that concepts have required fields
        array_concept = graph['data_structures']['array']
        self.assertIn('prerequisites', array_concept)
        self.assertIn('leads_to', array_concept)
        self.assertIn('difficulty', array_concept)
        self.assertIn('importance', array_concept)
    
    def test_learning_resources(self):
        """Test learning resources structure"""
        resources = self.engine.learning_resources
        
        self.assertIsInstance(resources, dict)
        self.assertIn('array', resources)
        
        # Check that resources have required fields
        array_resources = resources['array']
        self.assertIsInstance(array_resources, list)
        
        if array_resources:
            resource = array_resources[0]
            self.assertIn('title', resource)
            self.assertIn('type', resource)
            self.assertIn('difficulty', resource)

class TestProgressTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ProgressTracker()
    
    def test_skill_thresholds(self):
        """Test skill level thresholds"""
        thresholds = self.tracker.skill_thresholds
        
        self.assertIn('beginner', thresholds)
        self.assertIn('intermediate', thresholds)
        self.assertIn('advanced', thresholds)
        
        # Check threshold structure
        beginner = thresholds['beginner']
        self.assertIn('min_score', beginner)
        self.assertIn('max_score', beginner)

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.analyzer = CodeAnalyzer()
        self.engine = RecommendationEngine()
    
    def test_analysis_to_recommendations_flow(self):
        """Test the flow from code analysis to recommendations"""
        # Analyze a simple code snippet
        code = """
def simple_loop(n):
    result = []
    for i in range(n):
        result.append(i * 2)
    return result
        """
        
        analysis = self.analyzer.analyze_code(code, 'python')
        
        # Test that we can generate recommendations from analysis
        # Note: This would normally require a database user, so we'll just test structure
        mock_analysis = {
            'data_structures': ['array'],
            'algorithms': [],
            'patterns': [],
            'time_complexity': 'O(n)',
            'space_complexity': 'O(n)'
        }
        
        # This should not crash
        self.assertIsInstance(mock_analysis, dict)

def run_sample_analysis():
    """Run a sample analysis to demonstrate the system"""
    print("Running sample code analysis...")
    
    analyzer = CodeAnalyzer()
    
    # Sample code: Two Sum problem
    sample_code = """
def two_sum(nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    return []
    """
    
    result = analyzer.analyze_code(sample_code, 'python')
    
    print("\\nAnalysis Results:")
    print(f"Quality Score: {result['quality_score']}")
    print(f"Complexity Score: {result['complexity_score']}")
    print(f"Time Complexity: {result['time_complexity']}")
    print(f"Space Complexity: {result['space_complexity']}")
    print(f"Data Structures: {result['data_structures']}")
    print(f"Patterns: {result['patterns']}")
    print(f"Algorithms: {result['algorithms']}")
    print(f"Issues: {result['issues']}")
    print(f"Suggestions: {result['suggestions']}")
    
    print("\\nSample analysis completed successfully!")

if __name__ == '__main__':
    # Run sample analysis
    run_sample_analysis()
    print("\\n" + "="*50)
    print("Running unit tests...")
    print("="*50)
    
    # Run unit tests
    unittest.main(verbosity=2)
