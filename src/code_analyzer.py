import ast
import re
import json
from typing import Dict, List, Any
from collections import defaultdict

class CodeAnalyzer:
    def __init__(self):
        self.algorithm_patterns = {
            'dynamic_programming': [
                r'dp\[.*\]', r'memo\[.*\]', r'cache\[.*\]',
                r'@lru_cache', r'@cache', r'tabulation'
            ],
            'greedy': [
                r'greedy', r'local.*optimal', r'sort.*reverse',
                r'heappush', r'heappop', r'priority.*queue'
            ],
            'divide_and_conquer': [
                r'divide.*conquer', r'merge.*sort', r'quick.*sort',
                r'binary.*search', r'recursion.*half'
            ],
            'backtracking': [
                r'backtrack', r'dfs.*return', r'recursive.*choice',
                r'restore.*state', r'prune.*branch'
            ],
            'sliding_window': [
                r'sliding.*window', r'two.*pointer', r'left.*right',
                r'window.*size', r'expand.*contract'
            ],
            'tree_traversal': [
                r'inorder', r'preorder', r'postorder', r'level.*order',
                r'bfs', r'dfs', r'queue.*append', r'stack.*append'
            ],
            'graph_algorithms': [
                r'dijkstra', r'bellman.*ford', r'floyd.*warshall',
                r'union.*find', r'topological.*sort', r'adjacency'
            ]
        }
        
        self.data_structure_patterns = {
            'array': [r'list\[', r'array\[', r'\[\]', r'append\(', r'pop\('],
            'hash_table': [r'dict\(', r'defaultdict', r'Counter', r'set\('],
            'linked_list': [r'ListNode', r'next', r'head', r'tail'],
            'stack': [r'stack', r'append\(', r'pop\(', r'LIFO'],
            'queue': [r'queue', r'deque', r'popleft', r'appendleft', r'FIFO'],
            'heap': [r'heapq', r'heappush', r'heappop', r'priority.*queue'],
            'tree': [r'TreeNode', r'left', r'right', r'root', r'leaf'],
            'graph': [r'graph', r'adjacency', r'edges', r'vertices', r'neighbors']
        }
        
        self.complexity_indicators = {
            'time': {
                'O(1)': [r'constant.*time', r'single.*operation'],
                'O(log n)': [r'binary.*search', r'tree.*height', r'heap.*operation'],
                'O(n)': [r'linear.*search', r'single.*loop', r'one.*pass'],
                'O(n log n)': [r'merge.*sort', r'heap.*sort', r'sort\('],
                'O(n^2)': [r'nested.*loop', r'double.*loop', r'quadratic'],
                'O(2^n)': [r'exponential', r'all.*subsets', r'brute.*force']
            },
            'space': {
                'O(1)': [r'constant.*space', r'in.*place'],
                'O(n)': [r'auxiliary.*array', r'recursion.*stack', r'hash.*table'],
                'O(n^2)': [r'2d.*array', r'matrix', r'nested.*structure']
            }
        }

    def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code and return comprehensive analysis"""
        
        analysis = {
            'language': language,
            'complexity_score': 0.0,
            'quality_score': 0.0,
            'patterns': [],
            'algorithms': [],
            'data_structures': [],
            'time_complexity': 'Unknown',
            'space_complexity': 'Unknown',
            'metrics': {},
            'issues': [],
            'suggestions': []
        }
        
        if language.lower() == 'python':
            analysis = self._analyze_python_code(code, analysis)
        else:
            analysis = self._analyze_generic_code(code, analysis)
        
        # Calculate overall scores
        analysis['complexity_score'] = self._calculate_complexity_score(analysis)
        analysis['quality_score'] = self._calculate_quality_score(analysis)
        
        return analysis

    def _analyze_python_code(self, code: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze Python code using AST"""
        try:
            tree = ast.parse(code)
            
            # Basic metrics
            analysis['metrics']['lines_of_code'] = len(code.strip().split('\n'))
            analysis['metrics']['functions'] = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            analysis['metrics']['loops'] = len([node for node in ast.walk(tree) if isinstance(node, (ast.For, ast.While))])
            analysis['metrics']['conditionals'] = len([node for node in ast.walk(tree) if isinstance(node, ast.If)])
            
            # Cyclomatic complexity
            analysis['metrics']['cyclomatic_complexity'] = self._calculate_cyclomatic_complexity(tree)
            
            # Pattern detection
            analysis['patterns'] = self._detect_patterns(code)
            analysis['algorithms'] = self._detect_algorithms(code)
            analysis['data_structures'] = self._detect_data_structures(code)
            
            # Complexity estimation
            analysis['time_complexity'] = self._estimate_time_complexity(code, tree)
            analysis['space_complexity'] = self._estimate_space_complexity(code, tree)
            
            # Code quality issues
            analysis['issues'] = self._detect_code_issues(code, tree)
            analysis['suggestions'] = self._generate_suggestions(analysis)
            
        except SyntaxError as e:
            analysis['issues'].append(f"Syntax error: {str(e)}")
            analysis = self._analyze_generic_code(code, analysis)
        
        return analysis

    def _analyze_generic_code(self, code: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code without AST parsing"""
        
        # Basic metrics
        lines = code.strip().split('\n')
        analysis['metrics']['lines_of_code'] = len(lines)
        
        # Pattern detection using regex
        analysis['patterns'] = self._detect_patterns(code)
        analysis['algorithms'] = self._detect_algorithms(code)
        analysis['data_structures'] = self._detect_data_structures(code)
        
        # Complexity estimation
        analysis['time_complexity'] = self._estimate_time_complexity_regex(code)
        analysis['space_complexity'] = self._estimate_space_complexity_regex(code)
        
        return analysis

    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity

    def _detect_patterns(self, code: str) -> List[str]:
        """Detect coding patterns in the code"""
        patterns = []
        code_lower = code.lower()
        
        # Common patterns
        pattern_checks = {
            'two_pointers': ['left', 'right', 'start', 'end', 'i', 'j'],
            'sliding_window': ['window', 'left', 'right', 'expand', 'contract'],
            'fast_slow_pointers': ['slow', 'fast', 'tortoise', 'hare'],
            'merge_intervals': ['merge', 'interval', 'overlap', 'start', 'end'],
            'cyclic_sort': ['cycle', 'sort', 'position', 'place'],
            'tree_dfs': ['dfs', 'depth', 'recursive', 'left', 'right'],
            'tree_bfs': ['bfs', 'breadth', 'level', 'queue'],
            'topological_sort': ['topological', 'indegree', 'outdegree', 'kahn'],
            'binary_search': ['binary', 'search', 'mid', 'left', 'right'],
            'modified_binary_search': ['rotated', 'pivot', 'search', 'sorted']
        }
        
        for pattern, keywords in pattern_checks.items():
            if any(keyword in code_lower for keyword in keywords):
                patterns.append(pattern)
        
        return patterns

    def _detect_algorithms(self, code: str) -> List[str]:
        """Detect algorithms used in the code"""
        algorithms = []
        
        for algorithm, patterns in self.algorithm_patterns.items():
            for pattern in patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    algorithms.append(algorithm)
                    break
        
        return algorithms

    def _detect_data_structures(self, code: str) -> List[str]:
        """Detect data structures used in the code"""
        data_structures = []
        
        for ds, patterns in self.data_structure_patterns.items():
            for pattern in patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    data_structures.append(ds)
                    break
        
        return data_structures

    def _estimate_time_complexity(self, code: str, tree: ast.AST) -> str:
        """Estimate time complexity from AST"""
        # Count nested loops
        max_nesting = 0
        current_nesting = 0
        
        class LoopCounter(ast.NodeVisitor):
            def __init__(self):
                self.max_nesting = 0
                self.current_nesting = 0
            
            def visit_For(self, node):
                self.current_nesting += 1
                self.max_nesting = max(self.max_nesting, self.current_nesting)
                self.generic_visit(node)
                self.current_nesting -= 1
            
            def visit_While(self, node):
                self.current_nesting += 1
                self.max_nesting = max(self.max_nesting, self.current_nesting)
                self.generic_visit(node)
                self.current_nesting -= 1
        
        counter = LoopCounter()
        counter.visit(tree)
        
        # Estimate based on patterns
        if counter.max_nesting == 0:
            return "O(1)"
        elif counter.max_nesting == 1:
            if any(pattern in code.lower() for pattern in ['sort', 'heappush', 'heappop']):
                return "O(n log n)"
            else:
                return "O(n)"
        elif counter.max_nesting == 2:
            return "O(n^2)"
        else:
            return f"O(n^{counter.max_nesting})"

    def _estimate_space_complexity(self, code: str, tree: ast.AST) -> str:
        """Estimate space complexity from AST"""
        # Check for recursive calls
        has_recursion = any(isinstance(node, ast.Call) and 
                          isinstance(node.func, ast.Name) for node in ast.walk(tree))
        
        # Check for data structures
        if 'dict' in code or 'set' in code or 'list' in code:
            return "O(n)"
        elif has_recursion:
            return "O(n)"  # Recursion stack
        else:
            return "O(1)"

    def _estimate_time_complexity_regex(self, code: str) -> str:
        """Estimate time complexity using regex patterns"""
        for complexity, patterns in self.complexity_indicators['time'].items():
            for pattern in patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    return complexity
        return "O(n)"  # Default assumption

    def _estimate_space_complexity_regex(self, code: str) -> str:
        """Estimate space complexity using regex patterns"""
        for complexity, patterns in self.complexity_indicators['space'].items():
            for pattern in patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    return complexity
        return "O(1)"  # Default assumption

    def _detect_code_issues(self, code: str, tree: ast.AST) -> List[str]:
        """Detect potential code quality issues"""
        issues = []
        
        # Check for long functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_lines = len(ast.get_source_segment(code, node).split('\n'))
                if func_lines > 50:
                    issues.append(f"Function '{node.name}' is too long ({func_lines} lines)")
        
        # Check for deep nesting
        class NestingChecker(ast.NodeVisitor):
            def __init__(self):
                self.max_nesting = 0
                self.current_nesting = 0
            
            def visit_If(self, node):
                self.current_nesting += 1
                self.max_nesting = max(self.max_nesting, self.current_nesting)
                self.generic_visit(node)
                self.current_nesting -= 1
        
        checker = NestingChecker()
        checker.visit(tree)
        
        if checker.max_nesting > 4:
            issues.append(f"Deep nesting detected (level {checker.max_nesting})")
        
        # Check for variable naming
        if re.search(r'\b[a-z]\b', code):
            issues.append("Single letter variable names detected")
        
        return issues

    def _generate_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Complexity suggestions
        if analysis['time_complexity'] == 'O(n^2)':
            suggestions.append("Consider optimizing to O(n log n) using sorting or O(n) using hash table")
        
        # Algorithm suggestions
        if 'brute_force' in analysis['patterns']:
            suggestions.append("Consider using dynamic programming or greedy approach")
        
        # Data structure suggestions
        if 'array' in analysis['data_structures'] and 'lookup' in analysis['patterns']:
            suggestions.append("Consider using hash table for O(1) lookups")
        
        return suggestions

    def _calculate_complexity_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate complexity score (0-100)"""
        score = 100.0
        
        # Penalize high time complexity
        time_penalties = {
            'O(1)': 0, 'O(log n)': 0, 'O(n)': 5,
            'O(n log n)': 15, 'O(n^2)': 30, 'O(2^n)': 50
        }
        score -= time_penalties.get(analysis['time_complexity'], 20)
        
        # Penalize high cyclomatic complexity
        cyclomatic = analysis['metrics'].get('cyclomatic_complexity', 0)
        if cyclomatic > 10:
            score -= min(30, (cyclomatic - 10) * 3)
        
        # Penalize issues
        score -= len(analysis['issues']) * 5
        
        return max(0, score)

    def _calculate_quality_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate code quality score (0-100)"""
        score = 100.0
        
        # Penalize issues
        score -= len(analysis['issues']) * 10
        
        # Reward good patterns
        score += len(analysis['patterns']) * 5
        
        # Reward algorithm usage
        score += len(analysis['algorithms']) * 3
        
        return min(100, max(0, score))
