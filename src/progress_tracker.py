import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from models.database import db, User, Submission, ProgressMetric, KnowledgeGap

class ProgressTracker:
    def __init__(self):
        self.skill_thresholds = {
            'beginner': {'min_score': 0, 'max_score': 40},
            'intermediate': {'min_score': 40, 'max_score': 75},
            'advanced': {'min_score': 75, 'max_score': 100}
        }
        
    def get_user_progress(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive progress analytics for a user"""
        
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}
        
        # Get user submissions
        submissions = Submission.query.filter_by(user_id=user_id).order_by(Submission.submitted_at).all()
        
        if not submissions:
            return {
                'user_id': user_id,
                'total_submissions': 0,
                'progress_summary': 'No submissions yet',
                'recommendations': ['Start with basic array problems']
            }
        
        # Calculate various progress metrics
        progress_data = {
            'user_id': user_id,
            'username': user.username,
            'skill_level': user.skill_level,
            'total_submissions': len(submissions),
            'submission_analytics': self._analyze_submissions(submissions),
            'skill_progression': self._track_skill_progression(submissions),
            'concept_mastery': self._analyze_concept_mastery(user_id, submissions),
            'performance_trends': self._analyze_performance_trends(submissions),
            'learning_velocity': self._calculate_learning_velocity(submissions),
            'strengths_weaknesses': self._identify_strengths_weaknesses(submissions),
            'milestone_progress': self._track_milestones(submissions),
            'recommendations': self._generate_progress_recommendations(user_id, submissions)
        }
        
        return progress_data
    
    def _analyze_submissions(self, submissions: List[Submission]) -> Dict[str, Any]:
        """Analyze submission patterns and statistics"""
        
        if not submissions:
            return {}
        
        # Basic statistics
        total_submissions = len(submissions)
        avg_complexity_score = np.mean([s.complexity_score or 0 for s in submissions])
        avg_quality_score = np.mean([s.quality_score or 0 for s in submissions])
        
        # Language distribution
        language_counts = Counter([s.language for s in submissions])
        
        # Time analysis
        submission_dates = [s.submitted_at for s in submissions]
        date_range = (submission_dates[-1] - submission_dates[0]).days if len(submission_dates) > 1 else 0
        avg_submissions_per_week = (total_submissions / max(date_range, 1)) * 7
        
        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_submissions = [s for s in submissions if s.submitted_at >= thirty_days_ago]
        
        return {
            'total_submissions': total_submissions,
            'average_complexity_score': round(avg_complexity_score, 2),
            'average_quality_score': round(avg_quality_score, 2),
            'languages_used': dict(language_counts),
            'most_used_language': language_counts.most_common(1)[0][0] if language_counts else None,
            'submission_frequency': {
                'total_days_active': date_range,
                'average_per_week': round(avg_submissions_per_week, 2)
            },
            'recent_activity': {
                'submissions_last_30_days': len(recent_submissions),
                'avg_score_last_30_days': round(np.mean([s.quality_score or 0 for s in recent_submissions]), 2) if recent_submissions else 0
            }
        }
    
    def _track_skill_progression(self, submissions: List[Submission]) -> Dict[str, Any]:
        """Track how user's skills have progressed over time"""
        
        if len(submissions) < 2:
            return {'trend': 'insufficient_data'}
        
        # Group submissions by time periods
        submissions_by_week = defaultdict(list)
        
        for submission in submissions:
            week_key = submission.submitted_at.strftime('%Y-W%U')
            submissions_by_week[week_key].append(submission)
        
        # Calculate weekly averages
        weekly_scores = []
        weekly_dates = []
        
        for week, week_submissions in submissions_by_week.items():
            avg_quality = np.mean([s.quality_score or 0 for s in week_submissions])
            avg_complexity = np.mean([s.complexity_score or 0 for s in week_submissions])
            
            weekly_scores.append((avg_quality + avg_complexity) / 2)
            weekly_dates.append(week)
        
        # Calculate trend
        if len(weekly_scores) >= 2:
            x = np.arange(len(weekly_scores)).reshape(-1, 1)
            y = np.array(weekly_scores)
            
            model = LinearRegression()
            model.fit(x, y)
            
            trend_slope = model.coef_[0]
            trend_direction = 'improving' if trend_slope > 0.1 else 'declining' if trend_slope < -0.1 else 'stable'
            
            # Calculate improvement rate
            improvement_rate = ((weekly_scores[-1] - weekly_scores[0]) / weekly_scores[0]) * 100 if weekly_scores[0] > 0 else 0
        else:
            trend_direction = 'insufficient_data'
            improvement_rate = 0
        
        return {
            'trend': trend_direction,
            'improvement_rate_percentage': round(improvement_rate, 2),
            'weekly_average_scores': weekly_scores,
            'current_score': weekly_scores[-1] if weekly_scores else 0,
            'best_score': max(weekly_scores) if weekly_scores else 0,
            'consistency': self._calculate_consistency(weekly_scores)
        }
    
    def _analyze_concept_mastery(self, user_id: int, submissions: List[Submission]) -> Dict[str, Any]:
        """Analyze mastery level of different programming concepts"""
        
        concept_scores = defaultdict(list)
        concept_counts = defaultdict(int)
        
        # Collect scores for each concept
        for submission in submissions:
            # Data structures
            if submission.patterns_used:
                patterns = submission.patterns_used.split(',')
                for pattern in patterns:
                    pattern = pattern.strip()
                    if pattern:
                        concept_scores[pattern].append(submission.quality_score or 0)
                        concept_counts[pattern] += 1
            
            # Algorithms
            if submission.algorithms_identified:
                try:
                    algorithms = json.loads(submission.algorithms_identified)
                    for algorithm in algorithms:
                        concept_scores[algorithm].append(submission.quality_score or 0)
                        concept_counts[algorithm] += 1
                except json.JSONDecodeError:
                    pass
        
        # Calculate mastery levels
        concept_mastery = {}
        for concept, scores in concept_scores.items():
            avg_score = np.mean(scores)
            attempts = len(scores)
            
            # Determine mastery level
            if avg_score >= 80 and attempts >= 3:
                mastery_level = 'mastered'
            elif avg_score >= 60 and attempts >= 2:
                mastery_level = 'proficient'
            elif avg_score >= 40:
                mastery_level = 'learning'
            else:
                mastery_level = 'struggling'
            
            concept_mastery[concept] = {
                'mastery_level': mastery_level,
                'average_score': round(avg_score, 2),
                'attempts': attempts,
                'improvement_trend': self._calculate_concept_trend(scores)
            }
        
        # Identify knowledge gaps
        knowledge_gaps = KnowledgeGap.query.filter_by(user_id=user_id, status='identified').all()
        gap_concepts = [gap.concept for gap in knowledge_gaps]
        
        return {
            'concepts_analyzed': len(concept_mastery),
            'mastery_breakdown': concept_mastery,
            'mastered_concepts': [c for c, data in concept_mastery.items() if data['mastery_level'] == 'mastered'],
            'struggling_concepts': [c for c, data in concept_mastery.items() if data['mastery_level'] == 'struggling'],
            'knowledge_gaps': gap_concepts,
            'overall_mastery_score': self._calculate_overall_mastery(concept_mastery)
        }
    
    def _analyze_performance_trends(self, submissions: List[Submission]) -> Dict[str, Any]:
        """Analyze performance trends across different dimensions"""
        
        if len(submissions) < 3:
            return {'trend': 'insufficient_data'}
        
        # Performance by time complexity
        complexity_performance = defaultdict(list)
        for submission in submissions:
            if submission.time_complexity:
                complexity_performance[submission.time_complexity].append(submission.quality_score or 0)
        
        # Performance by problem difficulty (estimated from complexity scores)
        difficulty_performance = {'easy': [], 'medium': [], 'hard': []}
        for submission in submissions:
            complexity_score = submission.complexity_score or 0
            if complexity_score < 30:
                difficulty_performance['easy'].append(submission.quality_score or 0)
            elif complexity_score < 70:
                difficulty_performance['medium'].append(submission.quality_score or 0)
            else:
                difficulty_performance['hard'].append(submission.quality_score or 0)
        
        # Recent vs older performance
        mid_point = len(submissions) // 2
        older_submissions = submissions[:mid_point]
        recent_submissions = submissions[mid_point:]
        
        older_avg = np.mean([s.quality_score or 0 for s in older_submissions])
        recent_avg = np.mean([s.quality_score or 0 for s in recent_submissions])
        
        return {
            'performance_by_complexity': {
                complexity: {
                    'average_score': round(np.mean(scores), 2),
                    'attempts': len(scores)
                } for complexity, scores in complexity_performance.items() if scores
            },
            'performance_by_difficulty': {
                level: {
                    'average_score': round(np.mean(scores), 2),
                    'attempts': len(scores)
                } for level, scores in difficulty_performance.items() if scores
            },
            'temporal_comparison': {
                'older_period_average': round(older_avg, 2),
                'recent_period_average': round(recent_avg, 2),
                'improvement': round(recent_avg - older_avg, 2)
            }
        }
    
    def _calculate_learning_velocity(self, submissions: List[Submission]) -> Dict[str, Any]:
        """Calculate how quickly the user is learning and improving"""
        
        if len(submissions) < 5:
            return {'velocity': 'insufficient_data'}
        
        # Calculate score improvements over time
        scores = [s.quality_score or 0 for s in submissions]
        
        # Use rolling average to smooth out fluctuations
        window_size = min(5, len(scores) // 2)
        rolling_averages = []
        
        for i in range(window_size, len(scores) + 1):
            window = scores[i-window_size:i]
            rolling_averages.append(np.mean(window))
        
        if len(rolling_averages) < 2:
            return {'velocity': 'insufficient_data'}
        
        # Calculate velocity (improvement per submission)
        velocity = (rolling_averages[-1] - rolling_averages[0]) / len(rolling_averages)
        
        # Calculate time-based velocity (improvement per day)
        time_span = (submissions[-1].submitted_at - submissions[0].submitted_at).days
        time_velocity = velocity * len(submissions) / max(time_span, 1)
        
        # Classify velocity
        if velocity > 2:
            velocity_category = 'fast'
        elif velocity > 0.5:
            velocity_category = 'moderate'
        elif velocity > -0.5:
            velocity_category = 'slow'
        else:
            velocity_category = 'declining'
        
        return {
            'velocity_category': velocity_category,
            'score_improvement_per_submission': round(velocity, 2),
            'score_improvement_per_day': round(time_velocity, 2),
            'learning_acceleration': self._calculate_acceleration(rolling_averages),
            'projected_score_in_30_days': round(rolling_averages[-1] + (time_velocity * 30), 2)
        }
    
    def _identify_strengths_weaknesses(self, submissions: List[Submission]) -> Dict[str, Any]:
        """Identify user's coding strengths and weaknesses"""
        
        # Analyze performance by different aspects
        aspects = {
            'algorithmic_thinking': [],
            'code_quality': [],
            'optimization': [],
            'problem_solving': []
        }
        
        for submission in submissions:
            quality_score = submission.quality_score or 0
            complexity_score = submission.complexity_score or 0
            
            # Estimate different aspect scores based on available metrics
            aspects['code_quality'].append(quality_score)
            aspects['optimization'].append(complexity_score)
            aspects['algorithmic_thinking'].append((quality_score + complexity_score) / 2)
            aspects['problem_solving'].append(quality_score)  # Simplified
        
        # Calculate averages and identify strengths/weaknesses
        aspect_averages = {
            aspect: np.mean(scores) if scores else 0
            for aspect, scores in aspects.items()
        }
        
        # Sort by performance
        sorted_aspects = sorted(aspect_averages.items(), key=lambda x: x[1], reverse=True)
        
        strengths = [aspect for aspect, score in sorted_aspects[:2] if score > 60]
        weaknesses = [aspect for aspect, score in sorted_aspects[-2:] if score < 50]
        
        return {
            'aspect_scores': {aspect: round(score, 2) for aspect, score in aspect_averages.items()},
            'strengths': strengths,
            'weaknesses': weaknesses,
            'most_improved_aspect': self._find_most_improved_aspect(submissions),
            'recommendations': self._generate_aspect_recommendations(aspect_averages)
        }
    
    def _track_milestones(self, submissions: List[Submission]) -> Dict[str, Any]:
        """Track important learning milestones"""
        
        milestones = {
            'first_submission': submissions[0].submitted_at if submissions else None,
            'submissions_count': len(submissions),
            'milestones_achieved': []
        }
        
        # Define milestone criteria
        milestone_criteria = [
            (10, '10_submissions', 'Completed 10 coding problems'),
            (25, '25_submissions', 'Completed 25 coding problems'),
            (50, '50_submissions', 'Completed 50 coding problems'),
            (100, '100_submissions', 'Completed 100 coding problems')
        ]
        
        for count, milestone_id, description in milestone_criteria:
            if len(submissions) >= count:
                milestones['milestones_achieved'].append({
                    'id': milestone_id,
                    'description': description,
                    'achieved_date': submissions[count-1].submitted_at,
                    'celebration_worthy': True
                })
        
        # Performance milestones
        quality_scores = [s.quality_score or 0 for s in submissions]
        if quality_scores:
            max_score = max(quality_scores)
            
            score_milestones = [
                (60, 'first_good_score', 'Achieved first quality score above 60'),
                (80, 'first_great_score', 'Achieved first quality score above 80'),
                (90, 'excellence', 'Achieved excellence with score above 90')
            ]
            
            for threshold, milestone_id, description in score_milestones:
                if max_score >= threshold:
                    # Find when this milestone was first achieved
                    for i, submission in enumerate(submissions):
                        if (submission.quality_score or 0) >= threshold:
                            milestones['milestones_achieved'].append({
                                'id': milestone_id,
                                'description': description,
                                'achieved_date': submission.submitted_at,
                                'score': submission.quality_score
                            })
                            break
        
        return milestones
    
    def _generate_progress_recommendations(self, user_id: int, submissions: List[Submission]) -> List[str]:
        """Generate recommendations based on progress analysis"""
        
        recommendations = []
        
        if len(submissions) < 5:
            recommendations.append("Keep practicing! Try to solve at least 5 more problems to get better insights.")
            return recommendations
        
        # Analyze recent performance
        recent_submissions = submissions[-5:]
        recent_avg = np.mean([s.quality_score or 0 for s in recent_submissions])
        
        if recent_avg < 50:
            recommendations.append("Focus on understanding problem fundamentals before optimizing.")
            recommendations.append("Consider reviewing basic data structures and algorithms.")
        elif recent_avg < 70:
            recommendations.append("Good progress! Try to optimize your solutions for better time complexity.")
            recommendations.append("Practice more challenging problems to improve further.")
        else:
            recommendations.append("Excellent work! Consider exploring advanced algorithms and design patterns.")
            recommendations.append("You might be ready for system design problems.")
        
        # Frequency recommendations
        submission_dates = [s.submitted_at for s in submissions]
        if len(submission_dates) > 1:
            days_between = (submission_dates[-1] - submission_dates[0]).days
            frequency = len(submissions) / max(days_between, 1)
            
            if frequency < 0.2:  # Less than 1 per 5 days
                recommendations.append("Try to maintain a more consistent practice schedule.")
        
        return recommendations
    
    def record_progress_metric(self, user_id: int, metric_name: str, metric_value: float, 
                             metric_type: str = 'score', context: Dict = None) -> bool:
        """Record a progress metric for a user"""
        
        try:
            metric = ProgressMetric(
                user_id=user_id,
                metric_name=metric_name,
                metric_value=metric_value,
                metric_type=metric_type,
                context=json.dumps(context) if context else None
            )
            
            db.session.add(metric)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            return False
    
    # Helper methods
    def _calculate_consistency(self, scores: List[float]) -> float:
        """Calculate consistency score (lower standard deviation = higher consistency)"""
        if len(scores) < 2:
            return 0.0
        
        std_dev = np.std(scores)
        mean_score = np.mean(scores)
        
        # Normalize consistency (0-100 scale, higher is better)
        consistency = max(0, 100 - (std_dev / max(mean_score, 1)) * 100)
        return round(consistency, 2)
    
    def _calculate_concept_trend(self, scores: List[float]) -> str:
        """Calculate trend for a specific concept"""
        if len(scores) < 2:
            return 'insufficient_data'
        
        recent_scores = scores[-3:] if len(scores) >= 3 else scores
        older_scores = scores[:-3] if len(scores) >= 3 else []
        
        if not older_scores:
            return 'new_concept'
        
        recent_avg = np.mean(recent_scores)
        older_avg = np.mean(older_scores)
        
        improvement = recent_avg - older_avg
        
        if improvement > 5:
            return 'improving'
        elif improvement < -5:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_overall_mastery(self, concept_mastery: Dict[str, Dict]) -> float:
        """Calculate overall mastery score"""
        if not concept_mastery:
            return 0.0
        
        mastery_weights = {
            'mastered': 1.0,
            'proficient': 0.7,
            'learning': 0.4,
            'struggling': 0.1
        }
        
        total_weight = 0
        weighted_sum = 0
        
        for concept_data in concept_mastery.values():
            level = concept_data['mastery_level']
            weight = mastery_weights.get(level, 0)
            
            total_weight += 1
            weighted_sum += weight
        
        return round((weighted_sum / total_weight) * 100, 2) if total_weight > 0 else 0.0
    
    def _calculate_acceleration(self, scores: List[float]) -> str:
        """Calculate learning acceleration"""
        if len(scores) < 3:
            return 'insufficient_data'
        
        # Calculate second derivative (acceleration)
        velocities = [scores[i+1] - scores[i] for i in range(len(scores)-1)]
        
        if len(velocities) < 2:
            return 'insufficient_data'
        
        accelerations = [velocities[i+1] - velocities[i] for i in range(len(velocities)-1)]
        avg_acceleration = np.mean(accelerations)
        
        if avg_acceleration > 0.5:
            return 'accelerating'
        elif avg_acceleration < -0.5:
            return 'decelerating'
        else:
            return 'steady'
    
    def _find_most_improved_aspect(self, submissions: List[Submission]) -> str:
        """Find the aspect that has improved the most"""
        if len(submissions) < 4:
            return 'insufficient_data'
        
        mid_point = len(submissions) // 2
        older_submissions = submissions[:mid_point]
        recent_submissions = submissions[mid_point:]
        
        aspects = ['quality_score', 'complexity_score']
        improvements = {}
        
        for aspect in aspects:
            older_avg = np.mean([getattr(s, aspect) or 0 for s in older_submissions])
            recent_avg = np.mean([getattr(s, aspect) or 0 for s in recent_submissions])
            improvements[aspect] = recent_avg - older_avg
        
        most_improved = max(improvements.items(), key=lambda x: x[1])
        return most_improved[0] if most_improved[1] > 0 else 'none'
    
    def _generate_aspect_recommendations(self, aspect_averages: Dict[str, float]) -> List[str]:
        """Generate recommendations based on aspect performance"""
        recommendations = []
        
        for aspect, score in aspect_averages.items():
            if score < 40:
                if aspect == 'code_quality':
                    recommendations.append("Focus on writing cleaner, more readable code")
                elif aspect == 'optimization':
                    recommendations.append("Study algorithm optimization techniques")
                elif aspect == 'algorithmic_thinking':
                    recommendations.append("Practice breaking down problems into smaller steps")
                elif aspect == 'problem_solving':
                    recommendations.append("Work on systematic problem-solving approaches")
        
        return recommendations
