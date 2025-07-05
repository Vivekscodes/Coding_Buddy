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
        
        # Get user's learning profile
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}
        
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
        
        return {\n            'knowledge_gaps': knowledge_gaps,\n            'concepts_to_learn': concept_recommendations,\n            'recommended_resources': resource_recommendations,\n            'practice_problems': problem_recommendations,\n            'improvement_suggestions': improvement_suggestions,\n            'estimated_study_time': self._calculate_study_time(concept_recommendations)\n        }\n    \n    def _identify_knowledge_gaps(self, user_id: int, code_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:\n        \"\"\"Identify knowledge gaps based on code analysis and user history\"\"\"\n        gaps = []\n        \n        # Get user's submission history\n        submissions = Submission.query.filter_by(user_id=user_id).order_by(Submission.submitted_at.desc()).limit(10).all()\n        \n        # Analyze patterns in recent submissions\n        recent_patterns = []\n        recent_algorithms = []\n        \n        for submission in submissions:\n            if submission.patterns_used:\n                recent_patterns.extend(submission.patterns_used.split(','))\n            if submission.algorithms_identified:\n                try:\n                    algorithms = json.loads(submission.algorithms_identified)\n                    recent_algorithms.extend(algorithms)\n                except json.JSONDecodeError:\n                    pass\n        \n        # Identify missing fundamental concepts\n        fundamental_concepts = ['array', 'linked_list', 'hash_table', 'recursion']\n        user_concepts = set(code_analysis.get('data_structures', []) + code_analysis.get('algorithms', []))\n        \n        for concept in fundamental_concepts:\n            if concept not in user_concepts and concept not in recent_patterns:\n                gaps.append({\n                    'concept': concept,\n                    'category': 'fundamental',\n                    'severity': 'high',\n                    'reason': f'Missing fundamental concept: {concept}'\n                })\n        \n        # Identify complexity issues\n        if code_analysis.get('time_complexity') in ['O(n^2)', 'O(2^n)']:\n            gaps.append({\n                'concept': 'algorithmic_optimization',\n                'category': 'performance',\n                'severity': 'medium',\n                'reason': 'Code has suboptimal time complexity'\n            })\n        \n        # Identify pattern gaps\n        if 'array' in code_analysis.get('data_structures', []) and 'two_pointers' not in code_analysis.get('patterns', []):\n            gaps.append({\n                'concept': 'two_pointers',\n                'category': 'pattern',\n                'severity': 'medium',\n                'reason': 'Array problems can often be optimized with two pointers technique'\n            })\n        \n        return gaps\n    \n    def _recommend_concepts(self, user_id: int, knowledge_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:\n        \"\"\"Recommend concepts to learn based on knowledge gaps and prerequisites\"\"\"\n        recommendations = []\n        \n        # Get user's current skill level\n        user = User.query.get(user_id)\n        skill_level = user.skill_level if user else 'beginner'\n        \n        # Process each knowledge gap\n        for gap in knowledge_gaps:\n            concept = gap['concept']\n            \n            # Find the concept in knowledge graph\n            concept_info = self._find_concept_in_graph(concept)\n            \n            if concept_info:\n                # Check if prerequisites are met\n                prerequisites_met = self._check_prerequisites(user_id, concept_info.get('prerequisites', []))\n                \n                if prerequisites_met:\n                    recommendations.append({\n                        'concept': concept,\n                        'category': gap['category'],\n                        'priority': self._calculate_priority(gap, concept_info),\n                        'difficulty': concept_info.get('difficulty', 'intermediate'),\n                        'estimated_time': self._estimate_learning_time(concept, skill_level),\n                        'prerequisites': concept_info.get('prerequisites', []),\n                        'leads_to': concept_info.get('leads_to', [])\n                    })\n                else:\n                    # Add prerequisites first\n                    for prereq in concept_info.get('prerequisites', []):\n                        prereq_info = self._find_concept_in_graph(prereq)\n                        if prereq_info:\n                            recommendations.append({\n                                'concept': prereq,\n                                'category': 'prerequisite',\n                                'priority': 'high',\n                                'difficulty': prereq_info.get('difficulty', 'beginner'),\n                                'estimated_time': self._estimate_learning_time(prereq, skill_level),\n                                'reason': f'Prerequisite for {concept}'\n                            })\n        \n        # Sort by priority\n        recommendations.sort(key=lambda x: {\n            'high': 3, 'medium': 2, 'low': 1\n        }.get(x.get('priority', 'low'), 1), reverse=True)\n        \n        return recommendations[:5]  # Return top 5 recommendations\n    \n    def _recommend_resources(self, user_id: int, concept_recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:\n        \"\"\"Recommend learning resources for the suggested concepts\"\"\"\n        resources = []\n        \n        for concept_rec in concept_recommendations:\n            concept = concept_rec['concept']\n            difficulty = concept_rec['difficulty']\n            \n            # Get resources for this concept\n            concept_resources = self.learning_resources.get(concept, [])\n            \n            # Filter by difficulty\n            suitable_resources = [\n                resource for resource in concept_resources\n                if self._is_suitable_difficulty(resource.get('difficulty', 'intermediate'), difficulty)\n            ]\n            \n            # Add to recommendations\n            for resource in suitable_resources[:2]:  # Max 2 resources per concept\n                resources.append({\n                    'concept': concept,\n                    'title': resource['title'],\n                    'type': resource['type'],\n                    'url': resource['url'],\n                    'difficulty': resource['difficulty'],\n                    'estimated_time': resource['estimated_time'],\n                    'priority': concept_rec.get('priority', 'medium')\n                })\n        \n        return resources\n    \n    def _recommend_problems(self, user_id: int, knowledge_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:\n        \"\"\"Recommend practice problems based on knowledge gaps\"\"\"\n        problems = []\n        \n        # Problem recommendations based on gaps\n        problem_mapping = {\n            'array': [\n                {'title': 'Two Sum', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/two-sum/'},\n                {'title': 'Best Time to Buy and Sell Stock', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/best-time-to-buy-and-sell-stock/'}\n            ],\n            'linked_list': [\n                {'title': 'Reverse Linked List', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/reverse-linked-list/'},\n                {'title': 'Merge Two Sorted Lists', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/merge-two-sorted-lists/'}\n            ],\n            'dynamic_programming': [\n                {'title': 'Climbing Stairs', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/climbing-stairs/'},\n                {'title': 'House Robber', 'difficulty': 'medium', 'url': 'https://leetcode.com/problems/house-robber/'}\n            ],\n            'two_pointers': [\n                {'title': 'Valid Palindrome', 'difficulty': 'easy', 'url': 'https://leetcode.com/problems/valid-palindrome/'},\n                {'title': 'Container With Most Water', 'difficulty': 'medium', 'url': 'https://leetcode.com/problems/container-with-most-water/'}\n            ]\n        }\n        \n        for gap in knowledge_gaps:\n            concept = gap['concept']\n            if concept in problem_mapping:\n                for problem in problem_mapping[concept]:\n                    problems.append({\n                        'concept': concept,\n                        'title': problem['title'],\n                        'difficulty': problem['difficulty'],\n                        'url': problem['url'],\n                        'estimated_time': 30,  # Default 30 minutes\n                        'priority': gap['severity']\n                    })\n        \n        return problems[:8]  # Return top 8 problems\n    \n    def _generate_improvement_suggestions(self, code_analysis: Dict[str, Any], knowledge_gaps: List[Dict[str, Any]]) -> List[str]:\n        \"\"\"Generate specific improvement suggestions\"\"\"\n        suggestions = []\n        \n        # Add suggestions from code analysis\n        suggestions.extend(code_analysis.get('suggestions', []))\n        \n        # Add suggestions based on knowledge gaps\n        for gap in knowledge_gaps:\n            if gap['concept'] == 'two_pointers':\n                suggestions.append(\"Learn the two pointers technique to optimize array problems\")\n            elif gap['concept'] == 'dynamic_programming':\n                suggestions.append(\"Study dynamic programming patterns to solve optimization problems\")\n            elif gap['concept'] == 'hash_table':\n                suggestions.append(\"Use hash tables for O(1) lookups and to avoid nested loops\")\n        \n        # Add complexity-specific suggestions\n        if code_analysis.get('time_complexity') == 'O(n^2)':\n            suggestions.append(\"Consider using hash tables or two pointers to reduce time complexity\")\n        \n        return list(set(suggestions))  # Remove duplicates\n    \n    def generate_learning_path(self, user_id: int) -> Dict[str, Any]:\n        \"\"\"Generate a comprehensive learning path for the user\"\"\"\n        \n        user = User.query.get(user_id)\n        if not user:\n            return {'error': 'User not found'}\n        \n        # Get user's submission history\n        submissions = Submission.query.filter_by(user_id=user_id).all()\n        \n        # Analyze user's strengths and weaknesses\n        strengths, weaknesses = self._analyze_strengths_weaknesses(submissions)\n        \n        # Generate learning modules\n        learning_modules = self._generate_learning_modules(user.skill_level, weaknesses)\n        \n        # Create learning path\n        learning_path = {\n            'user_id': user_id,\n            'skill_level': user.skill_level,\n            'strengths': strengths,\n            'weaknesses': weaknesses,\n            'learning_modules': learning_modules,\n            'estimated_duration': sum(module['estimated_time'] for module in learning_modules),\n            'difficulty_progression': self._get_difficulty_progression(user.skill_level)\n        }\n        \n        return learning_path\n    \n    def get_learning_resources(self) -> Dict[str, Any]:\n        \"\"\"Get all available learning resources\"\"\"\n        return {\n            'resources_by_concept': self.learning_resources,\n            'total_concepts': len(self.learning_resources),\n            'difficulty_levels': ['beginner', 'intermediate', 'advanced'],\n            'resource_types': ['article', 'video', 'tutorial', 'problem', 'book']\n        }\n    \n    # Helper methods\n    def _find_concept_in_graph(self, concept: str) -> Dict[str, Any]:\n        \"\"\"Find concept information in the knowledge graph\"\"\"\n        for category in self.knowledge_graph.values():\n            if concept in category:\n                return category[concept]\n        return None\n    \n    def _check_prerequisites(self, user_id: int, prerequisites: List[str]) -> bool:\n        \"\"\"Check if user has mastered the prerequisites\"\"\"\n        if not prerequisites:\n            return True\n        \n        # Get user's submission history\n        submissions = Submission.query.filter_by(user_id=user_id).all()\n        \n        # Extract concepts from submissions\n        user_concepts = set()\n        for submission in submissions:\n            if submission.patterns_used:\n                user_concepts.update(submission.patterns_used.split(','))\n            if submission.algorithms_identified:\n                try:\n                    algorithms = json.loads(submission.algorithms_identified)\n                    user_concepts.update(algorithms)\n                except json.JSONDecodeError:\n                    pass\n        \n        # Check if all prerequisites are met\n        return all(prereq in user_concepts for prereq in prerequisites)\n    \n    def _calculate_priority(self, gap: Dict[str, Any], concept_info: Dict[str, Any]) -> str:\n        \"\"\"Calculate priority for a concept recommendation\"\"\"\n        severity = gap.get('severity', 'medium')\n        importance = concept_info.get('importance', 0.5)\n        \n        if severity == 'high' and importance > 0.8:\n            return 'high'\n        elif severity == 'high' or importance > 0.7:\n            return 'medium'\n        else:\n            return 'low'\n    \n    def _estimate_learning_time(self, concept: str, skill_level: str) -> int:\n        \"\"\"Estimate learning time for a concept based on skill level\"\"\"\n        base_times = {\n            'array': 60, 'linked_list': 90, 'hash_table': 120,\n            'recursion': 180, 'dynamic_programming': 300,\n            'two_pointers': 90, 'binary_search': 120\n        }\n        \n        multipliers = {\n            'beginner': 1.5, 'intermediate': 1.0, 'advanced': 0.7\n        }\n        \n        base_time = base_times.get(concept, 120)\n        multiplier = multipliers.get(skill_level, 1.0)\n        \n        return int(base_time * multiplier)\n    \n    def _is_suitable_difficulty(self, resource_difficulty: str, user_difficulty: str) -> bool:\n        \"\"\"Check if resource difficulty is suitable for user\"\"\"\n        difficulty_levels = ['beginner', 'intermediate', 'advanced']\n        \n        resource_level = difficulty_levels.index(resource_difficulty) if resource_difficulty in difficulty_levels else 1\n        user_level = difficulty_levels.index(user_difficulty) if user_difficulty in difficulty_levels else 1\n        \n        # Allow resources that are at most one level above user's level\n        return resource_level <= user_level + 1\n    \n    def _calculate_study_time(self, concept_recommendations: List[Dict[str, Any]]) -> int:\n        \"\"\"Calculate total estimated study time\"\"\"\n        return sum(rec.get('estimated_time', 120) for rec in concept_recommendations)\n    \n    def _analyze_strengths_weaknesses(self, submissions: List[Submission]) -> Tuple[List[str], List[str]]:\n        \"\"\"Analyze user's strengths and weaknesses from submissions\"\"\"\n        if not submissions:\n            return [], ['fundamentals']\n        \n        # Count patterns and algorithms used\n        pattern_counts = Counter()\n        algorithm_counts = Counter()\n        \n        for submission in submissions:\n            if submission.patterns_used:\n                patterns = submission.patterns_used.split(',')\n                pattern_counts.update(patterns)\n            \n            if submission.algorithms_identified:\n                try:\n                    algorithms = json.loads(submission.algorithms_identified)\n                    algorithm_counts.update(algorithms)\n                except json.JSONDecodeError:\n                    pass\n        \n        # Identify strengths (frequently used concepts)\n        strengths = [concept for concept, count in pattern_counts.most_common(3) if count > 1]\n        strengths.extend([concept for concept, count in algorithm_counts.most_common(3) if count > 1])\n        \n        # Identify weaknesses (missing fundamental concepts)\n        fundamental_concepts = ['array', 'linked_list', 'hash_table', 'recursion', 'dynamic_programming']\n        all_concepts = set(pattern_counts.keys()) | set(algorithm_counts.keys())\n        weaknesses = [concept for concept in fundamental_concepts if concept not in all_concepts]\n        \n        return strengths[:5], weaknesses[:5]\n    \n    def _generate_learning_modules(self, skill_level: str, weaknesses: List[str]) -> List[Dict[str, Any]]:\n        \"\"\"Generate learning modules based on skill level and weaknesses\"\"\"\n        modules = []\n        \n        # Add modules for weaknesses\n        for weakness in weaknesses:\n            concept_info = self._find_concept_in_graph(weakness)\n            if concept_info:\n                modules.append({\n                    'concept': weakness,\n                    'title': f'Master {weakness.replace(\"_\", \" \").title()}',\n                    'difficulty': concept_info.get('difficulty', 'intermediate'),\n                    'estimated_time': self._estimate_learning_time(weakness, skill_level),\n                    'resources': self.learning_resources.get(weakness, []),\n                    'prerequisites': concept_info.get('prerequisites', []),\n                    'learning_objectives': self._get_learning_objectives(weakness)\n                })\n        \n        # Add progressive modules based on skill level\n        if skill_level == 'beginner':\n            modules.extend(self._get_beginner_modules())\n        elif skill_level == 'intermediate':\n            modules.extend(self._get_intermediate_modules())\n        elif skill_level == 'advanced':\n            modules.extend(self._get_advanced_modules())\n        \n        return modules[:10]  # Limit to 10 modules\n    \n    def _get_learning_objectives(self, concept: str) -> List[str]:\n        \"\"\"Get learning objectives for a concept\"\"\"\n        objectives = {\n            'array': [\n                'Understand array operations and indexing',\n                'Learn to traverse arrays efficiently',\n                'Master array manipulation techniques'\n            ],\n            'linked_list': [\n                'Understand linked list structure and operations',\n                'Learn to traverse and manipulate linked lists',\n                'Master two-pointer techniques for linked lists'\n            ],\n            'dynamic_programming': [\n                'Understand the principle of optimal substructure',\n                'Learn to identify overlapping subproblems',\n                'Master memoization and tabulation techniques'\n            ]\n        }\n        return objectives.get(concept, [f'Master {concept.replace(\"_\", \" \")}'])\n    \n    def _get_beginner_modules(self) -> List[Dict[str, Any]]:\n        \"\"\"Get learning modules for beginners\"\"\"\n        return [\n            {\n                'concept': 'problem_solving_fundamentals',\n                'title': 'Problem Solving Fundamentals',\n                'difficulty': 'beginner',\n                'estimated_time': 120,\n                'learning_objectives': [\n                    'Understand problem-solving approach',\n                    'Learn to break down complex problems',\n                    'Practice basic algorithmic thinking'\n                ]\n            }\n        ]\n    \n    def _get_intermediate_modules(self) -> List[Dict[str, Any]]:\n        \"\"\"Get learning modules for intermediate learners\"\"\"\n        return [\n            {\n                'concept': 'algorithm_optimization',\n                'title': 'Algorithm Optimization Techniques',\n                'difficulty': 'intermediate',\n                'estimated_time': 180,\n                'learning_objectives': [\n                    'Learn to analyze time and space complexity',\n                    'Master optimization techniques',\n                    'Practice efficient algorithm design'\n                ]\n            }\n        ]\n    \n    def _get_advanced_modules(self) -> List[Dict[str, Any]]:\n        \"\"\"Get learning modules for advanced learners\"\"\"\n        return [\n            {\n                'concept': 'advanced_algorithms',\n                'title': 'Advanced Algorithm Design',\n                'difficulty': 'advanced',\n                'estimated_time': 240,\n                'learning_objectives': [\n                    'Master complex algorithmic patterns',\n                    'Learn advanced optimization techniques',\n                    'Practice system design principles'\n                ]\n            }\n        ]\n    \n    def _get_difficulty_progression(self, skill_level: str) -> List[str]:\n        \"\"\"Get difficulty progression for the user\"\"\"\n        return self.difficulty_progression.get(skill_level, ['easy', 'medium'])
