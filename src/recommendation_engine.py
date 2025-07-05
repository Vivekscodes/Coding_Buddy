import json
import numpy as np
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

from models.database import db, User, Submission, LearningPath, KnowledgeGap, Resource

class RecommendationEngine:
    def __init__(self):
        self.knowledge_graph = self._build_knowledge_graph()
        self.learning_resources = self._load_learning_resources()
        self.difficulty_progression = {
            'beginner': ['easy'],
            'intermediate': ['easy', 'medium'],
            'advanced': ['medium', 'hard']
        }
        
    def _build_knowledge_graph(self) -> Dict[str, Any]:
        """Build a knowledge graph of programming concepts and their relationships"""
        return {
            'data_structures': {
                'array': {
                    'prerequisites': [],
                    'leads_to': ['dynamic_programming', 'two_pointers', 'sliding_window'],
                    'difficulty': 'beginner',
                    'importance': 0.9
                },
                'linked_list': {
                    'prerequisites': ['array'],
                    'leads_to': ['stack', 'queue', 'tree'],
                    'difficulty': 'beginner',
                    'importance': 0.8
                },
                'stack': {
                    'prerequisites': ['linked_list'],
                    'leads_to': ['recursion', 'backtracking'],
                    'difficulty': 'intermediate',
                    'importance': 0.7
                },
                'queue': {
                    'prerequisites': ['linked_list'],
                    'leads_to': ['bfs', 'tree_traversal'],
                    'difficulty': 'intermediate',
                    'importance': 0.7
                },
                'hash_table': {
                    'prerequisites': ['array'],
                    'leads_to': ['two_sum', 'caching', 'memoization'],
                    'difficulty': 'intermediate',
                    'importance': 0.9
                },
                'heap': {
                    'prerequisites': ['array', 'tree'],
                    'leads_to': ['priority_queue', 'dijkstra', 'kth_element'],
                    'difficulty': 'advanced',
                    'importance': 0.8
                },
                'tree': {
                    'prerequisites': ['linked_list', 'recursion'],
                    'leads_to': ['bst', 'trie', 'segment_tree'],
                    'difficulty': 'intermediate',
                    'importance': 0.8
                },
                'graph': {
                    'prerequisites': ['tree', 'queue'],
                    'leads_to': ['dfs', 'bfs', 'shortest_path'],
                    'difficulty': 'advanced',
                    'importance': 0.9
                }
            },
            'algorithms': {
                'two_pointers': {
                    'prerequisites': ['array'],
                    'leads_to': ['sliding_window', 'merge_intervals'],
                    'difficulty': 'intermediate',
                    'importance': 0.8
                },
                'sliding_window': {
                    'prerequisites': ['two_pointers'],
                    'leads_to': ['substring_problems', 'optimization'],
                    'difficulty': 'intermediate',
                    'importance': 0.8
                },
                'binary_search': {
                    'prerequisites': ['array', 'recursion'],
                    'leads_to': ['search_optimization', 'divide_and_conquer'],
                    'difficulty': 'intermediate',
                    'importance': 0.9
                },
                'dynamic_programming': {
                    'prerequisites': ['recursion', 'memoization'],
                    'leads_to': ['optimization_problems', 'advanced_dp'],
                    'difficulty': 'advanced',
                    'importance': 0.9
                },
                'greedy': {
                    'prerequisites': ['array', 'sorting'],
                    'leads_to': ['optimization', 'graph_algorithms'],
                    'difficulty': 'intermediate',
                    'importance': 0.7
                },
                'backtracking': {
                    'prerequisites': ['recursion', 'dfs'],
                    'leads_to': ['combinatorics', 'constraint_satisfaction'],
                    'difficulty': 'advanced',
                    'importance': 0.8
                },
                'dfs': {
                    'prerequisites': ['tree', 'graph', 'recursion'],
                    'leads_to': ['backtracking', 'topological_sort'],
                    'difficulty': 'intermediate',
                    'importance': 0.8
                },
                'bfs': {
                    'prerequisites': ['tree', 'graph', 'queue'],
                    'leads_to': ['shortest_path', 'level_order'],
                    'difficulty': 'intermediate',
                    'importance': 0.8
                }
            },
            'patterns': {
                'recursion': {
                    'prerequisites': ['function_basics'],
                    'leads_to': ['tree_problems', 'dynamic_programming'],
                    'difficulty': 'intermediate',
                    'importance': 0.9
                },
                'memoization': {
                    'prerequisites': ['recursion', 'hash_table'],
                    'leads_to': ['dynamic_programming', 'optimization'],
                    'difficulty': 'intermediate',
                    'importance': 0.8
                }
            }
        }
    
    def _load_learning_resources(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load learning resources for different concepts"""
        return {
            'array': [
                {
                    'title': 'Array Fundamentals',
                    'type': 'article',
                    'url': 'https://example.com/array-fundamentals',
                    'difficulty': 'beginner',
                    'estimated_time': 30
                },
                {
                    'title': 'Two Sum Problem',
                    'type': 'problem',
                    'url': 'https://leetcode.com/problems/two-sum/',
                    'difficulty': 'easy',
                    'estimated_time': 20
                }
            ],
            'linked_list': [
                {
                    'title': 'Linked List Implementation',
                    'type': 'tutorial',
                    'url': 'https://example.com/linked-list-tutorial',
                    'difficulty': 'beginner',
                    'estimated_time': 45
                },
                {
                    'title': 'Reverse Linked List',
                    'type': 'problem',
                    'url': 'https://leetcode.com/problems/reverse-linked-list/',
                    'difficulty': 'easy',
                    'estimated_time': 25
                }
            ],
            'dynamic_programming': [
                {
                    'title': 'DP Patterns and Techniques',
                    'type': 'video',
                    'url': 'https://example.com/dp-patterns',
                    'difficulty': 'advanced',
                    'estimated_time': 120
                },
                {
                    'title': 'Climbing Stairs',
                    'type': 'problem',
                    'url': 'https://leetcode.com/problems/climbing-stairs/',
                    'difficulty': 'easy',
                    'estimated_time': 15
                }
            ],
            'binary_search': [
                {
                    'title': 'Binary Search Template',
                    'type': 'article',
                    'url': 'https://example.com/binary-search-template',
                    'difficulty': 'intermediate',
                    'estimated_time': 40
                },
                {
                    'title': 'Search Insert Position',
                    'type': 'problem',
                    'url': 'https://leetcode.com/problems/search-insert-position/',
                    'difficulty': 'easy',
                    'estimated_time': 20
                }
            ]
        }
    
    def generate_recommendations(self, user_id: int, code_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized recommendations based on code analysis"""
        
        # Handle anonymous users
        if user_id is None:
            return self._generate_anonymous_recommendations(code_analysis)
        
        # Get user's learning profile
        user = User.query.get(user_id)
        if not user:
            return self._generate_anonymous_recommendations(code_analysis)
        
        # Analyze knowledge gaps
        knowledge_gaps = self._identify_knowledge_gaps(user_id, code_analysis)
        
        # Generate learning recommendations
        concept_recommendations = self._recommend_concepts(user_id, knowledge_gaps)
        
        # Recommend resources
        resource_recommendations = self._recommend_resources(user_id, concept_recommendations)
        
        # Recommend practice problems
        problem_recommendations = self._recommend_problems(user_id, knowledge_gaps)
        
        # Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(code_analysis, knowledge_gaps)
        
        return {
            'knowledge_gaps': knowledge_gaps,
            'concepts_to_learn': concept_recommendations,
            'recommended_resources': resource_recommendations,
            'practice_problems': problem_recommendations,
            'improvement_suggestions': improvement_suggestions,
            'estimated_study_time': self._calculate_study_time(concept_recommendations)
        }
    
    def _generate_anonymous_recommendations(self, code_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations for anonymous users based only on code analysis"""
        
        # Basic knowledge gaps analysis
        knowledge_gaps = self._identify_anonymous_knowledge_gaps(code_analysis)
        
        # Simple concept recommendations
        concept_recommendations = self._recommend_anonymous_concepts(knowledge_gaps)
        
        # Basic problem recommendations
        problem_recommendations = self._recommend_anonymous_problems(knowledge_gaps)
        
        # Simple improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(code_analysis, knowledge_gaps)
        
        return {
            'knowledge_gaps': knowledge_gaps,
            'concepts_to_learn': concept_recommendations,
            'practice_problems': problem_recommendations,
            'improvement_suggestions': improvement_suggestions,
            'estimated_study_time': self._calculate_anonymous_study_time(concept_recommendations)
        }
    
    def _identify_knowledge_gaps(self, user_id: int, code_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify knowledge gaps based on code analysis and user history"""
        gaps = []
        
        # Get user's submission history
        submissions = Submission.query.filter_by(user_id=user_id).order_by(Submission.submitted_at.desc()).limit(10).all()
        
        # Analyze patterns in recent submissions
        recent_patterns = []
        recent_algorithms = []
        
        for submission in submissions:
            if submission.patterns_used:
                recent_patterns.extend(submission.patterns_used.split(','))
            if submission.algorithms_identified:
                try:
                    algorithms = json.loads(submission.algorithms_identified)
                    recent_algorithms.extend(algorithms)
                except json.JSONDecodeError:
                    pass
        
        # Identify missing fundamental concepts
        fundamental_concepts = ['array', 'linked_list', 'hash_table', 'recursion']
        user_concepts = set(code_analysis.get('data_structures', []) + code_analysis.get('algorithms', []))
        
        for concept in fundamental_concepts:
            if concept not in user_concepts and concept not in recent_patterns:
                gaps.append({
                    'concept': concept,
                    'category': 'fundamental',
                    'severity': 'high',
                    'reason': f'Missing fundamental concept: {concept}'
                })
        
        # Identify complexity issues
        if code_analysis.get('time_complexity') in ['O(n^2)', 'O(2^n)']:
            gaps.append({
                'concept': 'algorithmic_optimization',
                'category': 'performance',
                'severity': 'medium',
                'reason': 'Code has suboptimal time complexity'
            })
        
        # Identify pattern gaps
        if 'array' in code_analysis.get('data_structures', []) and 'two_pointers' not in code_analysis.get('patterns', []):
            gaps.append({
                'concept': 'two_pointers',
                'category': 'pattern',
                'severity': 'medium',
                'reason': 'Array problems can often be optimized with two pointers technique'
            })
        
        return gaps
    
    def _recommend_concepts(self, user_id: int, knowledge_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Recommend concepts to learn based on knowledge gaps and prerequisites"""
        recommendations = []
        
        # Get user's current skill level
        user = User.query.get(user_id)
        skill_level = user.skill_level if user else 'beginner'
        
        # Process each knowledge gap
        for gap in knowledge_gaps:
            concept = gap['concept']
            
            # Find the concept in knowledge graph
            concept_info = self._find_concept_in_graph(concept)
            
            if concept_info:
                # Check if prerequisites are met
                prerequisites_met = self._check_prerequisites(user_id, concept_info.get('prerequisites', []))
                
                if prerequisites_met:
                    recommendations.append({
                        'concept': concept,
                        'category': gap['category'],
                        'priority': self._calculate_priority(gap, concept_info),
                        'difficulty': concept_info.get('difficulty', 'intermediate'),
                        'estimated_time': self._estimate_learning_time(concept, skill_level),
                        'prerequisites': concept_info.get('prerequisites', []),
                        'leads_to': concept_info.get('leads_to', [])
                    })
                else:
                    # Add prerequisites first
                    for prereq in concept_info.get('prerequisites', []):
                        prereq_info = self._find_concept_in_graph(prereq)
                        if prereq_info:
                            recommendations.append({
                                'concept': prereq,
                                'category': 'prerequisite',
                                'priority': 'high',
                                'difficulty': prereq_info.get('difficulty', 'beginner'),
                                'estimated_time': self._estimate_learning_time(prereq, skill_level),
                                'reason': f'Prerequisite for {concept}'
                            })
        
        # Sort by priority
        recommendations.sort(key=lambda x: {
            'high': 3, 'medium': 2, 'low': 1
        }.get(x.get('priority', 'low'), 1), reverse=True)
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _recommend_resources(self, user_id: int, concept_recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Recommend learning resources for the suggested concepts"""
        resources = []
        
        for concept_rec in concept_recommendations:
            concept = concept_rec['concept']
            difficulty = concept_rec['difficulty']
            
            # Get resources for this concept
            concept_resources = self.learning_resources.get(concept, [])
            
            # Filter by difficulty
            suitable_resources = [
                resource for resource in concept_resources
                if self._is_suitable_difficulty(resource.get('difficulty', 'intermediate'), difficulty)
            ]
            
            # Add to recommendations
            for resource in suitable_resources[:2]:  # Max 2 resources per concept
                resources.append({
                    'concept': concept,
                    'title': resource['title'],
                    'type': resource['type'],
                    'url': resource['url'],
                    'difficulty': resource['difficulty'],
                    'estimated_time': resource['estimated_time'],
                    'priority': concept_rec.get('priority', 'medium')
                })
        
        return resources
    
    def _recommend_problems(self, user_id: int, knowledge_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Recommend practice problems based on knowledge gaps"""
        problems = []
        
        # Problem recommendations based on gaps
        problem_mapping = {
            'array': [
                {'title': 'Two Sum', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/two-sum/'},
                {'title': 'Best Time to Buy and Sell Stock', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/best-time-to-buy-and-sell-stock/'}
            ],
            'linked_list': [
                {'title': 'Reverse Linked List', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/reverse-linked-list/'},
                {'title': 'Merge Two Sorted Lists', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/merge-two-sorted-lists/'}
            ],
            'dynamic_programming': [
                {'title': 'Climbing Stairs', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/climbing-stairs/'},
                {'title': 'House Robber', 'difficulty': 'medium', 'url': 'https://leetcode.com/problems/house-robber/'}
            ],
            'two_pointers': [
                {'title': 'Valid Palindrome', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/valid-palindrome/'},
                {'title': 'Container With Most Water', 'difficulty': 'medium', 'url': 'https://leetcode.com/problems/container-with-most-water/'}
            ]
        }
        
        for gap in knowledge_gaps:
            concept = gap['concept']
            if concept in problem_mapping:
                for problem in problem_mapping[concept]:
                    problems.append({
                        'concept': concept,
                        'title': problem['title'],
                        'difficulty': problem['difficulty'],
                        'url': problem['url'],
                        'estimated_time': 30,  # Default 30 minutes
                        'priority': gap['severity']
                    })
        
        return problems[:8]  # Return top 8 problems
    
    def _generate_improvement_suggestions(self, code_analysis: Dict[str, Any], knowledge_gaps: List[Dict[str, Any]]) -> List[str]:
        """Generate specific improvement suggestions"""
        suggestions = []
        
        # Add suggestions from code analysis
        suggestions.extend(code_analysis.get('suggestions', []))
        
        # Add suggestions based on knowledge gaps
        for gap in knowledge_gaps:
            if gap['concept'] == 'two_pointers':
                suggestions.append("Learn the two pointers technique to optimize array problems")
            elif gap['concept'] == 'dynamic_programming':
                suggestions.append("Study dynamic programming patterns to solve optimization problems")
            elif gap['concept'] == 'hash_table':
                suggestions.append("Use hash tables for O(1) lookups and to avoid nested loops")
        
        # Add complexity-specific suggestions
        if code_analysis.get('time_complexity') == 'O(n^2)':
            suggestions.append("Consider using hash tables or two pointers to reduce time complexity")
        
        return list(set(suggestions))  # Remove duplicates
    
    def generate_learning_path(self, user_id: int) -> Dict[str, Any]:
        """Generate a comprehensive learning path for the user"""
        
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}
        
        # Get user's submission history
        submissions = Submission.query.filter_by(user_id=user_id).all()
        
        # Analyze user's strengths and weaknesses
        strengths, weaknesses = self._analyze_strengths_weaknesses(submissions)
        
        # Generate learning modules
        learning_modules = self._generate_learning_modules(user.skill_level, weaknesses)
        
        # Create learning path
        learning_path = {
            'user_id': user_id,
            'skill_level': user.skill_level,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'learning_modules': learning_modules,
            'estimated_duration': sum(module['estimated_time'] for module in learning_modules),
            'difficulty_progression': self._get_difficulty_progression(user.skill_level)
        }
        
        return learning_path
    
    def _identify_anonymous_knowledge_gaps(self, code_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify knowledge gaps for anonymous users based only on code analysis"""
        gaps = []
        
        # Identify missing fundamental concepts
        fundamental_concepts = ['array', 'linked_list', 'hash_table', 'recursion']
        user_concepts = set(code_analysis.get('data_structures', []) + code_analysis.get('algorithms', []))
        
        for concept in fundamental_concepts:
            if concept not in user_concepts:
                gaps.append({
                    'concept': concept,
                    'category': 'fundamental',
                    'severity': 'high',
                    'reason': f'Missing fundamental concept: {concept}'
                })
        
        # Identify complexity issues
        if code_analysis.get('time_complexity') in ['O(n^2)', 'O(2^n)']:
            gaps.append({
                'concept': 'algorithmic_optimization',
                'category': 'performance',
                'severity': 'medium',
                'reason': 'Code has suboptimal time complexity'
            })
        
        # Identify pattern gaps
        if 'array' in code_analysis.get('data_structures', []) and 'two_pointers' not in code_analysis.get('patterns', []):
            gaps.append({
                'concept': 'two_pointers',
                'category': 'pattern',
                'severity': 'medium',
                'reason': 'Array problems can often be optimized with two pointers technique'
            })
        
        return gaps
    
    def _recommend_anonymous_concepts(self, knowledge_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Recommend concepts for anonymous users"""
        recommendations = []
        
        for gap in knowledge_gaps:
            concept = gap['concept']
            concept_info = self._find_concept_in_graph(concept)
            
            if concept_info:
                recommendations.append({
                    'concept': concept,
                    'category': gap['category'],
                    'difficulty': concept_info.get('difficulty', 'intermediate'),
                    'estimated_time': self._estimate_learning_time(concept, 'beginner')
                })
        
        return recommendations[:5]
    
    def _recommend_anonymous_problems(self, knowledge_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Recommend problems for anonymous users"""
        problems = []
        
        problem_mapping = {
            'array': [
                {'title': 'Two Sum', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/two-sum/', 'concept': 'array'},
                {'title': 'Best Time to Buy and Sell Stock', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/best-time-to-buy-and-sell-stock/', 'concept': 'array'}
            ],
            'linked_list': [
                {'title': 'Reverse Linked List', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/reverse-linked-list/', 'concept': 'linked_list'},
                {'title': 'Merge Two Sorted Lists', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/merge-two-sorted-lists/', 'concept': 'linked_list'}
            ],
            'hash_table': [
                {'title': 'Valid Anagram', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/valid-anagram/', 'concept': 'hash_table'},
                {'title': 'Group Anagrams', 'difficulty': 'medium', 'url': 'https://leetcode.com/problems/group-anagrams/', 'concept': 'hash_table'}
            ]
        }
        
        for gap in knowledge_gaps:
            concept = gap['concept']
            if concept in problem_mapping:
                problems.extend(problem_mapping[concept])
        
        return problems[:6]
    
    def _calculate_anonymous_study_time(self, concept_recommendations: List[Dict[str, Any]]) -> int:
        """Calculate estimated study time for anonymous users"""
        return sum(rec.get('estimated_time', 60) for rec in concept_recommendations)
    
    def get_learning_resources(self) -> Dict[str, Any]:
        """Get all available learning resources"""
        return {
            'resources_by_concept': self.learning_resources,
            'total_concepts': len(self.learning_resources),
            'difficulty_levels': ['beginner', 'intermediate', 'advanced'],
            'resource_types': ['article', 'video', 'tutorial', 'problem', 'book']
        }
    
    # Helper methods
    def _find_concept_in_graph(self, concept: str) -> Dict[str, Any]:
        """Find concept information in the knowledge graph"""
        for category in self.knowledge_graph.values():
            if concept in category:
                return category[concept]
        return None
    
    def _check_prerequisites(self, user_id: int, prerequisites: List[str]) -> bool:
        """Check if user has mastered the prerequisites"""
        if not prerequisites:
            return True
        
        # Get user's submission history
        submissions = Submission.query.filter_by(user_id=user_id).all()
        
        # Extract concepts from submissions
        user_concepts = set()
        for submission in submissions:
            if submission.patterns_used:
                user_concepts.update(submission.patterns_used.split(','))
            if submission.algorithms_identified:
                try:
                    algorithms = json.loads(submission.algorithms_identified)
                    user_concepts.update(algorithms)
                except json.JSONDecodeError:
                    pass
        
        # Check if all prerequisites are met
        return all(prereq in user_concepts for prereq in prerequisites)
    
    def _calculate_priority(self, gap: Dict[str, Any], concept_info: Dict[str, Any]) -> str:
        """Calculate priority for a concept recommendation"""
        severity = gap.get('severity', 'medium')
        importance = concept_info.get('importance', 0.5)
        
        if severity == 'high' and importance > 0.8:
            return 'high'
        elif severity == 'high' or importance > 0.7:
            return 'medium'
        else:
            return 'low'
    
    def _estimate_learning_time(self, concept: str, skill_level: str) -> int:
        """Estimate learning time for a concept based on skill level"""
        base_times = {
            'array': 60, 'linked_list': 90, 'hash_table': 120,
            'recursion': 180, 'dynamic_programming': 300,
            'two_pointers': 90, 'binary_search': 120
        }
        
        multipliers = {
            'beginner': 1.5, 'intermediate': 1.0, 'advanced': 0.7
        }
        
        base_time = base_times.get(concept, 120)
        multiplier = multipliers.get(skill_level, 1.0)
        
        return int(base_time * multiplier)
    
    def _is_suitable_difficulty(self, resource_difficulty: str, user_difficulty: str) -> bool:
        """Check if resource difficulty is suitable for user"""
        difficulty_levels = ['beginner', 'intermediate', 'advanced']
        
        resource_level = difficulty_levels.index(resource_difficulty) if resource_difficulty in difficulty_levels else 1
        user_level = difficulty_levels.index(user_difficulty) if user_difficulty in difficulty_levels else 1
        
        # Allow resources that are at most one level above user's level
        return resource_level <= user_level + 1
    
    def _calculate_study_time(self, concept_recommendations: List[Dict[str, Any]]) -> int:
        """Calculate total estimated study time"""
        return sum(rec.get('estimated_time', 120) for rec in concept_recommendations)
    
    def _analyze_strengths_weaknesses(self, submissions: List[Submission]) -> Tuple[List[str], List[str]]:
        """Analyze user's strengths and weaknesses from submissions"""
        if not submissions:
            return [], ['fundamentals']
        
        # Count patterns and algorithms used
        pattern_counts = Counter()
        algorithm_counts = Counter()
        
        for submission in submissions:
            if submission.patterns_used:
                patterns = submission.patterns_used.split(',')
                pattern_counts.update(patterns)
            
            if submission.algorithms_identified:
                try:
                    algorithms = json.loads(submission.algorithms_identified)
                    algorithm_counts.update(algorithms)
                except json.JSONDecodeError:
                    pass
        
        # Identify strengths (frequently used concepts)
        strengths = [concept for concept, count in pattern_counts.most_common(3) if count > 1]
        strengths.extend([concept for concept, count in algorithm_counts.most_common(3) if count > 1])
        
        # Identify weaknesses (missing fundamental concepts)
        fundamental_concepts = ['array', 'linked_list', 'hash_table', 'recursion', 'dynamic_programming']
        all_concepts = set(pattern_counts.keys()) | set(algorithm_counts.keys())
        weaknesses = [concept for concept in fundamental_concepts if concept not in all_concepts]
        
        return strengths[:5], weaknesses[:5]
    
    def _generate_learning_modules(self, skill_level: str, weaknesses: List[str]) -> List[Dict[str, Any]]:
        """Generate learning modules based on skill level and weaknesses"""
        modules = []
        
        # Add modules for weaknesses
        for weakness in weaknesses:
            concept_info = self._find_concept_in_graph(weakness)
            if concept_info:
                modules.append({
                    'concept': weakness,
                    'title': f'Master {weakness.replace("_", " ").title()}',
                    'difficulty': concept_info.get('difficulty', 'intermediate'),
                    'estimated_time': self._estimate_learning_time(weakness, skill_level),
                    'resources': self.learning_resources.get(weakness, []),
                    'prerequisites': concept_info.get('prerequisites', []),
                    'learning_objectives': self._get_learning_objectives(weakness)
                })
        
        # Add progressive modules based on skill level
        if skill_level == 'beginner':
            modules.extend(self._get_beginner_modules())
        elif skill_level == 'intermediate':
            modules.extend(self._get_intermediate_modules())
        elif skill_level == 'advanced':
            modules.extend(self._get_advanced_modules())
        
        return modules[:10]  # Limit to 10 modules
    
    def _get_learning_objectives(self, concept: str) -> List[str]:
        """Get learning objectives for a concept"""
        objectives = {
            'array': [
                'Understand array operations and indexing',
                'Learn to traverse arrays efficiently',
                'Master array manipulation techniques'
            ],
            'linked_list': [
                'Understand linked list structure and operations',
                'Learn to traverse and manipulate linked lists',
                'Master two-pointer techniques for linked lists'
            ],
            'dynamic_programming': [
                'Understand the principle of optimal substructure',
                'Learn to identify overlapping subproblems',
                'Master memoization and tabulation techniques'
            ]
        }
        return objectives.get(concept, [f'Master {concept.replace("_", " ")}'])
    
    def _get_beginner_modules(self) -> List[Dict[str, Any]]:
        """Get learning modules for beginners"""
        return [
            {
                'concept': 'problem_solving_fundamentals',
                'title': 'Problem Solving Fundamentals',
                'difficulty': 'beginner',
                'estimated_time': 120,
                'learning_objectives': [
                    'Understand problem-solving approach',
                    'Learn to break down complex problems',
                    'Practice basic algorithmic thinking'
                ]
            }
        ]
    
    def _get_intermediate_modules(self) -> List[Dict[str, Any]]:
        """Get learning modules for intermediate learners"""
        return [
            {
                'concept': 'algorithm_optimization',
                'title': 'Algorithm Optimization Techniques',
                'difficulty': 'intermediate',
                'estimated_time': 180,
                'learning_objectives': [
                    'Learn to analyze time and space complexity',
                    'Master optimization techniques',
                    'Practice efficient algorithm design'
                ]
            }
        ]
    
    def _get_advanced_modules(self) -> List[Dict[str, Any]]:
        """Get learning modules for advanced learners"""
        return [
            {
                'concept': 'advanced_algorithms',
                'title': 'Advanced Algorithm Design',
                'difficulty': 'advanced',
                'estimated_time': 240,
                'learning_objectives': [
                    'Master complex algorithmic patterns',
                    'Learn advanced optimization techniques',
                    'Practice system design principles'
                ]
            }
        ]
    
    def _get_difficulty_progression(self, skill_level: str) -> List[str]:
        """Get difficulty progression for the user"""
        return self.difficulty_progression.get(skill_level, ['easy', 'medium'])
