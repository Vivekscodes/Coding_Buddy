"""
Enhanced Learning Tracker
========================

This module provides comprehensive tracking of learning recommendations,
user progress, and learning outcomes. It integrates with the LLM-enhanced
code analyzer to provide data-driven learning insights.
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

from models.database import db, User, Submission, LearningPath, KnowledgeGap, ProgressMetric


class EnhancedLearningTracker:
    def __init__(self):
        self.learning_analytics = LearningAnalytics()
        self.recommendation_tracker = RecommendationTracker()
        self.progress_predictor = ProgressPredictor()
        
    def track_code_analysis_session(self, user_id: Optional[int], submission_id: int, 
                                  analysis_results: Dict[str, Any], 
                                  recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track a complete code analysis session including:
        - Code analysis results
        - Generated recommendations
        - User interaction with recommendations
        - Learning outcomes
        """
        session_data = {
            'session_id': f"session_{datetime.utcnow().isoformat()}",
            'user_id': user_id,
            'submission_id': submission_id,
            'timestamp': datetime.utcnow(),
            'analysis_results': analysis_results,
            'recommendations': recommendations,
            'tracking_metrics': {}
        }
        
        # Track recommendation effectiveness
        if user_id:
            self._track_recommendation_relevance(user_id, recommendations)
            self._update_learning_progress(user_id, analysis_results)
            self._track_skill_development(user_id, analysis_results)
        
        # Track anonymous user patterns
        else:
            self._track_anonymous_patterns(analysis_results, recommendations)
        
        # Generate learning insights
        learning_insights = self._generate_learning_insights(analysis_results, recommendations)
        session_data['learning_insights'] = learning_insights
        
        # Store session data
        self._store_session_data(session_data)
        
        return session_data
    
    def get_recommendation_effectiveness(self, user_id: int, 
                                       timeframe_days: int = 30) -> Dict[str, Any]:
        """
        Analyze the effectiveness of recommendations given to a user
        """
        return self.recommendation_tracker.analyze_effectiveness(user_id, timeframe_days)
    
    def get_learning_trajectory(self, user_id: int) -> Dict[str, Any]:
        """
        Get detailed learning trajectory analysis for a user
        """
        return self.learning_analytics.analyze_learning_trajectory(user_id)
    
    def predict_learning_outcomes(self, user_id: int, 
                                 proposed_learning_path: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict learning outcomes for a proposed learning path
        """
        return self.progress_predictor.predict_outcomes(user_id, proposed_learning_path)
    
    def get_comprehensive_analytics(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get comprehensive learning analytics
        """
        if user_id:
            return self._get_user_analytics(user_id)
        else:
            return self._get_system_analytics()
    
    def _track_recommendation_relevance(self, user_id: int, recommendations: Dict[str, Any]):
        """Track how relevant recommendations are to user's current skill level"""
        # Store recommendation for later effectiveness analysis
        recommendation_record = {
            'user_id': user_id,
            'recommendations': recommendations,
            'generated_at': datetime.utcnow(),
            'type': 'code_analysis_recommendation'
        }
        
        self.recommendation_tracker.store_recommendation(recommendation_record)
    
    def _update_learning_progress(self, user_id: int, analysis_results: Dict[str, Any]):
        """Update user's learning progress based on code analysis"""
        
        # Extract skill indicators from analysis
        complexity_score = analysis_results.get('complexity_score', 0)
        quality_score = analysis_results.get('quality_score', 0)
        patterns_used = analysis_results.get('patterns', [])
        algorithms_used = analysis_results.get('algorithms', [])
        
        # Update progress metrics
        self._record_progress_metric(user_id, 'complexity_handling', complexity_score)
        self._record_progress_metric(user_id, 'code_quality', quality_score)
        self._record_progress_metric(user_id, 'pattern_diversity', len(set(patterns_used)))
        self._record_progress_metric(user_id, 'algorithm_diversity', len(set(algorithms_used)))
        
        # Update skill level if significant improvement detected
        self._evaluate_skill_level_progression(user_id)
    
    def _track_skill_development(self, user_id: int, analysis_results: Dict[str, Any]):
        """Track development of specific programming skills"""
        
        skills_demonstrated = []
        
        # Analyze demonstrated skills
        if analysis_results.get('time_complexity') in ['O(log n)', 'O(n log n)']:
            skills_demonstrated.append('algorithmic_optimization')
        
        if analysis_results.get('quality_score', 0) > 8:
            skills_demonstrated.append('clean_code')
        
        if len(analysis_results.get('patterns', [])) > 2:
            skills_demonstrated.append('pattern_recognition')
        
        # Record demonstrated skills
        for skill in skills_demonstrated:
            self._record_progress_metric(user_id, f'skill_{skill}', 1, 'count')
    
    def _track_anonymous_patterns(self, analysis_results: Dict[str, Any], 
                                 recommendations: Dict[str, Any]):
        """Track patterns for anonymous users to improve system recommendations"""
        
        # Store anonymous patterns for system improvement
        anonymous_data = {
            'timestamp': datetime.utcnow(),
            'complexity_score': analysis_results.get('complexity_score', 0),
            'quality_score': analysis_results.get('quality_score', 0),
            'patterns_count': len(analysis_results.get('patterns', [])),
            'algorithms_count': len(analysis_results.get('algorithms', [])),
            'recommendations_count': len(recommendations.get('concepts_to_learn', [])),
            'language': analysis_results.get('language', 'unknown')
        }
        
        # This could be stored in a separate analytics table for system improvement
        self._store_anonymous_analytics(anonymous_data)
    
    def _generate_learning_insights(self, analysis_results: Dict[str, Any], 
                                   recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate actionable learning insights from analysis and recommendations"""
        
        insights = {
            'strengths_identified': [],
            'areas_for_improvement': [],
            'learning_priorities': [],
            'estimated_learning_time': 0,
            'personalized_tips': []
        }
        
        # Identify strengths
        if analysis_results.get('quality_score', 0) > 7:
            insights['strengths_identified'].append('Good code quality and structure')
        
        if len(analysis_results.get('patterns', [])) > 1:
            insights['strengths_identified'].append('Demonstrates multiple programming patterns')
        
        # Identify areas for improvement
        knowledge_gaps = recommendations.get('knowledge_gaps', [])
        for gap in knowledge_gaps:
            insights['areas_for_improvement'].append(gap.get('reason', 'General improvement needed'))
        
        # Set learning priorities
        concepts_to_learn = recommendations.get('concepts_to_learn', [])
        high_priority_concepts = [c for c in concepts_to_learn if c.get('priority') == 'high']
        insights['learning_priorities'] = [c['concept'] for c in high_priority_concepts]
        
        # Calculate learning time
        insights['estimated_learning_time'] = recommendations.get('estimated_study_time', 0)
        
        # Generate personalized tips
        insights['personalized_tips'] = self._generate_personalized_tips(analysis_results, recommendations)
        
        return insights
    
    def _generate_personalized_tips(self, analysis_results: Dict[str, Any], 
                                   recommendations: Dict[str, Any]) -> List[str]:
        """Generate personalized learning tips"""
        tips = []
        
        # Tips based on complexity
        if analysis_results.get('time_complexity') == 'O(n^2)':
            tips.append("Focus on learning optimization techniques like hash tables or two pointers")
        
        # Tips based on patterns
        patterns = analysis_results.get('patterns', [])
        if 'array' in patterns and 'two_pointers' not in patterns:
            tips.append("Practice two pointers technique to optimize array problems")
        
        # Tips based on quality
        if analysis_results.get('quality_score', 0) < 6:
            tips.append("Focus on code readability and proper naming conventions")
        
        # Tips based on recommendations
        if recommendations.get('knowledge_gaps'):
            gap_concepts = [gap['concept'] for gap in recommendations['knowledge_gaps']]
            if 'recursion' in gap_concepts:
                tips.append("Start with simple recursive problems before tackling complex ones")
        
        return tips
    
    def _record_progress_metric(self, user_id: int, metric_name: str, 
                               metric_value: float, metric_type: str = 'score'):
        """Record a progress metric for a user"""
        
        metric = ProgressMetric(
            user_id=user_id,
            metric_name=metric_name,
            metric_value=metric_value,
            metric_type=metric_type,
            recorded_at=datetime.utcnow()
        )
        
        try:
            db.session.add(metric)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error recording progress metric: {e}")
    
    def _evaluate_skill_level_progression(self, user_id: int):
        """Evaluate if user should progress to next skill level"""
        
        # Get recent metrics
        recent_metrics = ProgressMetric.query.filter_by(user_id=user_id)\
            .filter(ProgressMetric.recorded_at >= datetime.utcnow() - timedelta(days=30))\
            .all()
        
        if not recent_metrics:
            return
        
        # Calculate average scores
        quality_scores = [m.metric_value for m in recent_metrics if m.metric_name == 'code_quality']
        complexity_scores = [m.metric_value for m in recent_metrics if m.metric_name == 'complexity_handling']
        
        if quality_scores and complexity_scores:
            avg_quality = np.mean(quality_scores)
            avg_complexity = np.mean(complexity_scores)
            
            # Check for skill level progression
            user = User.query.get(user_id)
            if user:
                current_level = user.skill_level
                
                if current_level == 'beginner' and avg_quality > 7 and avg_complexity > 6:
                    user.skill_level = 'intermediate'
                    self._record_progress_metric(user_id, 'skill_level_progression', 2, 'level')
                elif current_level == 'intermediate' and avg_quality > 8.5 and avg_complexity > 8:
                    user.skill_level = 'advanced'
                    self._record_progress_metric(user_id, 'skill_level_progression', 3, 'level')
                
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Error updating skill level: {e}")
    
    def _store_session_data(self, session_data: Dict[str, Any]):
        """Store complete session data for analytics"""
        # This could be stored in a dedicated sessions table
        # For now, we'll store key metrics as progress metrics
        
        user_id = session_data.get('user_id')
        if user_id:
            session_id = session_data['session_id']
            
            # Store session summary metrics
            analysis_results = session_data['analysis_results']
            recommendations = session_data['recommendations']
            
            context = {
                'session_id': session_id,
                'recommendations_count': len(recommendations.get('concepts_to_learn', [])),
                'knowledge_gaps_count': len(recommendations.get('knowledge_gaps', [])),
                'estimated_study_time': recommendations.get('estimated_study_time', 0)
            }
            
            self._record_progress_metric(
                user_id, 
                'learning_session', 
                1, 
                'count'
            )
    
    def _store_anonymous_analytics(self, anonymous_data: Dict[str, Any]):
        """Store anonymous user analytics for system improvement"""
        # This would typically go to a separate analytics storage
        # For now, we'll just log it
        print(f"Anonymous analytics: {anonymous_data}")
    
    def _get_user_analytics(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive analytics for a specific user"""
        
        # Get user info
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}
        
        # Get learning trajectory
        trajectory = self.learning_analytics.analyze_learning_trajectory(user_id)
        
        # Get recommendation effectiveness
        recommendation_effectiveness = self.recommendation_tracker.analyze_effectiveness(user_id, 30)
        
        # Get recent progress
        recent_progress = self._get_recent_progress(user_id, 30)
        
        return {
            'user_profile': {
                'username': user.username,
                'skill_level': user.skill_level,
                'member_since': user.created_at.isoformat(),
                'total_submissions': len(user.submissions)
            },
            'learning_trajectory': trajectory,
            'recommendation_effectiveness': recommendation_effectiveness,
            'recent_progress': recent_progress,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def _get_system_analytics(self) -> Dict[str, Any]:
        """Get system-wide analytics"""
        
        # Get overall system metrics
        total_users = User.query.count()
        total_submissions = Submission.query.count()
        total_sessions = ProgressMetric.query.filter_by(metric_name='learning_session').count()
        
        # Get language distribution
        language_distribution = self._get_language_distribution()
        
        # Get skill level distribution
        skill_distribution = self._get_skill_distribution()
        
        return {
            'system_overview': {
                'total_users': total_users,
                'total_submissions': total_submissions,
                'total_learning_sessions': total_sessions,
                'generated_at': datetime.utcnow().isoformat()
            },
            'distributions': {
                'languages': language_distribution,
                'skill_levels': skill_distribution
            }
        }
    
    def _get_recent_progress(self, user_id: int, days: int) -> Dict[str, Any]:
        """Get user's recent progress metrics"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        recent_metrics = ProgressMetric.query.filter_by(user_id=user_id)\
            .filter(ProgressMetric.recorded_at >= cutoff_date)\
            .order_by(ProgressMetric.recorded_at.desc())\
            .all()
        
        # Group metrics by type
        metrics_by_type = defaultdict(list)
        for metric in recent_metrics:
            metrics_by_type[metric.metric_name].append({
                'value': metric.metric_value,
                'recorded_at': metric.recorded_at.isoformat()
            })
        
        return dict(metrics_by_type)
    
    def _get_language_distribution(self) -> Dict[str, int]:
        """Get distribution of programming languages used"""
        
        submissions = Submission.query.all()
        language_counts = Counter(sub.language for sub in submissions)
        
        return dict(language_counts)
    
    def _get_skill_distribution(self) -> Dict[str, int]:
        """Get distribution of user skill levels"""
        
        users = User.query.all()
        skill_counts = Counter(user.skill_level for user in users)
        
        return dict(skill_counts)


class LearningAnalytics:
    """Advanced analytics for learning patterns and trajectories"""
    
    def analyze_learning_trajectory(self, user_id: int) -> Dict[str, Any]:
        """Analyze user's learning trajectory over time"""
        
        # Get user's progress metrics over time
        metrics = ProgressMetric.query.filter_by(user_id=user_id)\
            .order_by(ProgressMetric.recorded_at.asc())\
            .all()
        
        if not metrics:
            return {'trajectory': 'insufficient_data'}
        
        # Analyze different aspects of learning
        quality_trend = self._analyze_quality_trend(metrics)
        complexity_trend = self._analyze_complexity_trend(metrics)
        skill_development = self._analyze_skill_development(metrics)
        learning_velocity = self._calculate_learning_velocity(metrics)
        
        return {
            'quality_trend': quality_trend,
            'complexity_trend': complexity_trend,
            'skill_development': skill_development,
            'learning_velocity': learning_velocity,
            'overall_trajectory': self._classify_trajectory(quality_trend, complexity_trend)
        }
    
    def _analyze_quality_trend(self, metrics: List[ProgressMetric]) -> Dict[str, Any]:
        """Analyze code quality improvement trend"""
        
        quality_metrics = [m for m in metrics if m.metric_name == 'code_quality']
        
        if len(quality_metrics) < 2:
            return {'trend': 'insufficient_data'}
        
        values = [m.metric_value for m in quality_metrics]
        timestamps = [m.recorded_at for m in quality_metrics]
        
        # Calculate trend
        trend_slope = np.polyfit(range(len(values)), values, 1)[0]
        
        return {
            'trend': 'improving' if trend_slope > 0.1 else 'stable' if abs(trend_slope) <= 0.1 else 'declining',
            'slope': trend_slope,
            'current_average': np.mean(values[-5:]) if len(values) >= 5 else np.mean(values),
            'improvement_rate': trend_slope * 30  # Monthly improvement rate
        }
    
    def _analyze_complexity_trend(self, metrics: List[ProgressMetric]) -> Dict[str, Any]:
        """Analyze complexity handling improvement trend"""
        
        complexity_metrics = [m for m in metrics if m.metric_name == 'complexity_handling']
        
        if len(complexity_metrics) < 2:
            return {'trend': 'insufficient_data'}
        
        values = [m.metric_value for m in complexity_metrics]
        trend_slope = np.polyfit(range(len(values)), values, 1)[0]
        
        return {
            'trend': 'improving' if trend_slope > 0.1 else 'stable' if abs(trend_slope) <= 0.1 else 'declining',
            'slope': trend_slope,
            'current_level': np.mean(values[-3:]) if len(values) >= 3 else np.mean(values)
        }
    
    def _analyze_skill_development(self, metrics: List[ProgressMetric]) -> Dict[str, Any]:
        """Analyze development of specific skills"""
        
        skill_metrics = [m for m in metrics if m.metric_name.startswith('skill_')]
        
        skills_progress = defaultdict(int)
        for metric in skill_metrics:
            skill_name = metric.metric_name.replace('skill_', '')
            skills_progress[skill_name] += metric.metric_value
        
        return dict(skills_progress)
    
    def _calculate_learning_velocity(self, metrics: List[ProgressMetric]) -> Dict[str, Any]:
        """Calculate learning velocity (rate of progress)"""
        
        if len(metrics) < 2:
            return {'velocity': 'insufficient_data'}
        
        # Calculate metrics per week
        first_date = metrics[0].recorded_at
        last_date = metrics[-1].recorded_at
        weeks_span = (last_date - first_date).days / 7
        
        if weeks_span < 1:
            return {'velocity': 'insufficient_timespan'}
        
        sessions_per_week = len([m for m in metrics if m.metric_name == 'learning_session']) / weeks_span
        
        return {
            'sessions_per_week': sessions_per_week,
            'total_weeks_active': weeks_span,
            'velocity_category': self._categorize_velocity(sessions_per_week)
        }
    
    def _categorize_velocity(self, sessions_per_week: float) -> str:
        """Categorize learning velocity"""
        if sessions_per_week >= 5:
            return 'high'
        elif sessions_per_week >= 2:
            return 'moderate'
        elif sessions_per_week >= 0.5:
            return 'low'
        else:
            return 'very_low'
    
    def _classify_trajectory(self, quality_trend: Dict, complexity_trend: Dict) -> str:
        """Classify overall learning trajectory"""
        
        if quality_trend.get('trend') == 'improving' and complexity_trend.get('trend') == 'improving':
            return 'excellent_progress'
        elif quality_trend.get('trend') == 'improving' or complexity_trend.get('trend') == 'improving':
            return 'good_progress'
        elif quality_trend.get('trend') == 'stable' and complexity_trend.get('trend') == 'stable':
            return 'steady_state'
        else:
            return 'needs_attention'


class RecommendationTracker:
    """Track effectiveness and impact of learning recommendations"""
    
    def __init__(self):
        self.recommendations_storage = []  # In production, this would be a database table
    
    def store_recommendation(self, recommendation_record: Dict[str, Any]):
        """Store a recommendation record for later analysis"""
        self.recommendations_storage.append(recommendation_record)
    
    def analyze_effectiveness(self, user_id: int, timeframe_days: int) -> Dict[str, Any]:
        """Analyze effectiveness of recommendations for a user"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=timeframe_days)
        
        # Get recommendations in timeframe
        user_recommendations = [
            r for r in self.recommendations_storage 
            if r['user_id'] == user_id and r['generated_at'] >= cutoff_date
        ]
        
        if not user_recommendations:
            return {'effectiveness': 'no_recommendations'}
        
        # Analyze improvement after recommendations
        improvement_metrics = self._analyze_post_recommendation_improvement(user_id, user_recommendations)
        
        # Analyze recommendation relevance
        relevance_metrics = self._analyze_recommendation_relevance(user_id, user_recommendations)
        
        return {
            'total_recommendations': len(user_recommendations),
            'improvement_metrics': improvement_metrics,
            'relevance_metrics': relevance_metrics,
            'overall_effectiveness': self._calculate_overall_effectiveness(improvement_metrics, relevance_metrics)
        }
    
    def _analyze_post_recommendation_improvement(self, user_id: int, 
                                               recommendations: List[Dict]) -> Dict[str, Any]:
        """Analyze improvement in metrics after recommendations"""
        
        improvement_scores = []
        
        for rec in recommendations:
            rec_date = rec['generated_at']
            
            # Get metrics before and after recommendation
            before_metrics = ProgressMetric.query.filter_by(user_id=user_id)\
                .filter(ProgressMetric.recorded_at < rec_date)\
                .filter(ProgressMetric.recorded_at >= rec_date - timedelta(days=7))\
                .all()
            
            after_metrics = ProgressMetric.query.filter_by(user_id=user_id)\
                .filter(ProgressMetric.recorded_at > rec_date)\
                .filter(ProgressMetric.recorded_at <= rec_date + timedelta(days=14))\
                .all()
            
            if before_metrics and after_metrics:
                improvement = self._calculate_improvement_score(before_metrics, after_metrics)
                improvement_scores.append(improvement)
        
        if improvement_scores:
            return {
                'average_improvement': np.mean(improvement_scores),
                'improvement_rate': len([s for s in improvement_scores if s > 0]) / len(improvement_scores),
                'sample_size': len(improvement_scores)
            }
        else:
            return {'improvement_analysis': 'insufficient_data'}
    
    def _analyze_recommendation_relevance(self, user_id: int, 
                                        recommendations: List[Dict]) -> Dict[str, Any]:
        """Analyze how relevant recommendations were to user's actual needs"""
        
        # This would analyze if recommended concepts were actually used in subsequent submissions
        # For now, returning placeholder metrics
        
        return {
            'relevance_score': 0.75,  # Placeholder
            'concepts_adopted': 3,     # Placeholder
            'concepts_recommended': 5  # Placeholder
        }
    
    def _calculate_improvement_score(self, before_metrics: List[ProgressMetric], 
                                   after_metrics: List[ProgressMetric]) -> float:
        """Calculate improvement score between before and after metrics"""
        
        # Calculate average quality and complexity scores before and after
        before_quality = np.mean([m.metric_value for m in before_metrics if m.metric_name == 'code_quality'])
        after_quality = np.mean([m.metric_value for m in after_metrics if m.metric_name == 'code_quality'])
        
        before_complexity = np.mean([m.metric_value for m in before_metrics if m.metric_name == 'complexity_handling'])
        after_complexity = np.mean([m.metric_value for m in after_metrics if m.metric_name == 'complexity_handling'])
        
        # Calculate improvement (positive is better)
        quality_improvement = after_quality - before_quality
        complexity_improvement = after_complexity - before_complexity
        
        # Weighted average improvement
        return (quality_improvement * 0.6 + complexity_improvement * 0.4)
    
    def _calculate_overall_effectiveness(self, improvement_metrics: Dict, 
                                       relevance_metrics: Dict) -> str:
        """Calculate overall effectiveness rating"""
        
        if improvement_metrics.get('improvement_analysis') == 'insufficient_data':
            return 'insufficient_data'
        
        avg_improvement = improvement_metrics.get('average_improvement', 0)
        improvement_rate = improvement_metrics.get('improvement_rate', 0)
        relevance_score = relevance_metrics.get('relevance_score', 0)
        
        # Calculate composite score
        effectiveness_score = (avg_improvement * 0.4 + improvement_rate * 0.3 + relevance_score * 0.3)
        
        if effectiveness_score >= 0.7:
            return 'highly_effective'
        elif effectiveness_score >= 0.5:
            return 'moderately_effective'
        elif effectiveness_score >= 0.3:
            return 'somewhat_effective'
        else:
            return 'low_effectiveness'


class ProgressPredictor:
    """Predict learning outcomes and progress"""
    
    def predict_outcomes(self, user_id: int, 
                        proposed_learning_path: Dict[str, Any]) -> Dict[str, Any]:
        """Predict learning outcomes for a proposed learning path"""
        
        # Get user's historical data
        user_metrics = ProgressMetric.query.filter_by(user_id=user_id).all()
        
        if len(user_metrics) < 5:
            return {'prediction': 'insufficient_historical_data'}
        
        # Analyze learning patterns
        learning_patterns = self._analyze_learning_patterns(user_metrics)
        
        # Predict completion time
        predicted_completion_time = self._predict_completion_time(
            learning_patterns, proposed_learning_path
        )
        
        # Predict success probability
        success_probability = self._predict_success_probability(
            learning_patterns, proposed_learning_path
        )
        
        # Generate recommendations for optimization
        optimization_suggestions = self._generate_optimization_suggestions(
            learning_patterns, proposed_learning_path
        )
        
        return {
            'predicted_completion_time': predicted_completion_time,
            'success_probability': success_probability,
            'learning_patterns': learning_patterns,
            'optimization_suggestions': optimization_suggestions
        }
    
    def _analyze_learning_patterns(self, metrics: List[ProgressMetric]) -> Dict[str, Any]:
        """Analyze user's learning patterns from historical data"""
        
        # Calculate learning velocity
        sessions = [m for m in metrics if m.metric_name == 'learning_session']
        if len(sessions) >= 2:
            time_between_sessions = [(sessions[i].recorded_at - sessions[i-1].recorded_at).days 
                                   for i in range(1, len(sessions))]
            avg_session_interval = np.mean(time_between_sessions)
        else:
            avg_session_interval = 7  # Default to weekly
        
        # Calculate improvement rate
        quality_metrics = [m for m in metrics if m.metric_name == 'code_quality']
        if len(quality_metrics) >= 3:
            values = [m.metric_value for m in quality_metrics]
            improvement_rate = np.polyfit(range(len(values)), values, 1)[0]
        else:
            improvement_rate = 0.1  # Default slow improvement
        
        return {
            'average_session_interval_days': avg_session_interval,
            'improvement_rate': improvement_rate,
            'total_sessions': len(sessions),
            'learning_consistency': self._calculate_consistency(sessions)
        }
    
    def _calculate_consistency(self, sessions: List[ProgressMetric]) -> float:
        """Calculate learning consistency score"""
        if len(sessions) < 3:
            return 0.5
        
        intervals = [(sessions[i].recorded_at - sessions[i-1].recorded_at).days 
                    for i in range(1, len(sessions))]
        
        # Lower standard deviation indicates higher consistency
        consistency = 1 / (1 + np.std(intervals))
        return min(consistency, 1.0)
    
    def _predict_completion_time(self, learning_patterns: Dict, 
                               learning_path: Dict) -> Dict[str, Any]:
        """Predict completion time for learning path"""
        
        estimated_hours = learning_path.get('estimated_duration', 40)
        session_interval = learning_patterns['average_session_interval_days']
        improvement_rate = learning_patterns['improvement_rate']
        
        # Adjust based on user's learning patterns
        if improvement_rate > 0.2:  # Fast learner
            time_multiplier = 0.8
        elif improvement_rate < 0.05:  # Slow learner
            time_multiplier = 1.3
        else:
            time_multiplier = 1.0
        
        predicted_days = (estimated_hours / 2) * session_interval * time_multiplier
        
        return {
            'estimated_days': int(predicted_days),
            'estimated_weeks': int(predicted_days / 7),
            'confidence': 'medium' if len(learning_patterns) > 10 else 'low'
        }
    
    def _predict_success_probability(self, learning_patterns: Dict, 
                                   learning_path: Dict) -> Dict[str, Any]:
        """Predict probability of successfully completing learning path"""
        
        consistency = learning_patterns['learning_consistency']
        improvement_rate = learning_patterns['improvement_rate']
        total_sessions = learning_patterns['total_sessions']
        
        # Calculate base probability
        base_probability = 0.5
        
        # Adjust based on patterns
        if consistency > 0.7:
            base_probability += 0.2
        if improvement_rate > 0.1:
            base_probability += 0.15
        if total_sessions > 20:
            base_probability += 0.1
        
        # Adjust based on path difficulty
        path_difficulty = learning_path.get('difficulty_level', 'intermediate')
        if path_difficulty == 'advanced':
            base_probability -= 0.15
        elif path_difficulty == 'beginner':
            base_probability += 0.1
        
        success_probability = max(0.1, min(0.95, base_probability))
        
        return {
            'probability': success_probability,
            'confidence_level': self._get_confidence_level(success_probability),
            'key_factors': self._identify_key_factors(learning_patterns)
        }
    
    def _get_confidence_level(self, probability: float) -> str:
        """Get confidence level for prediction"""
        if probability >= 0.8:
            return 'high'
        elif probability >= 0.6:
            return 'medium'
        else:
            return 'low'
    
    def _identify_key_factors(self, learning_patterns: Dict) -> List[str]:
        """Identify key factors affecting success probability"""
        factors = []
        
        if learning_patterns['learning_consistency'] > 0.7:
            factors.append('consistent_learning_schedule')
        if learning_patterns['improvement_rate'] > 0.1:
            factors.append('good_improvement_rate')
        if learning_patterns['total_sessions'] > 20:
            factors.append('sufficient_experience')
        
        return factors
    
    def _generate_optimization_suggestions(self, learning_patterns: Dict, 
                                         learning_path: Dict) -> List[str]:
        """Generate suggestions to optimize learning path"""
        suggestions = []
        
        if learning_patterns['learning_consistency'] < 0.5:
            suggestions.append('Establish a more consistent learning schedule')
        
        if learning_patterns['improvement_rate'] < 0.05:
            suggestions.append('Consider breaking down complex topics into smaller modules')
        
        if learning_patterns['average_session_interval_days'] > 10:
            suggestions.append('Try to reduce time between learning sessions for better retention')
        
        return suggestions
