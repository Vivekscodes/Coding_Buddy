from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Learning profile
    skill_level = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced
    preferred_languages = db.Column(db.Text)  # JSON string of preferred languages
    learning_goals = db.Column(db.Text)  # JSON string of learning goals
    
    # Relationships
    submissions = db.relationship('Submission', backref='user', lazy=True)
    learning_paths = db.relationship('LearningPath', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Allow anonymous submissions
    problem_title = db.Column(db.String(200), nullable=False)
    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    
    # Analysis results
    complexity_score = db.Column(db.Float, default=0.0)
    quality_score = db.Column(db.Float, default=0.0)
    patterns_used = db.Column(db.Text)  # Comma-separated patterns
    algorithms_identified = db.Column(db.Text)  # JSON string
    
    # Metrics
    lines_of_code = db.Column(db.Integer, default=0)
    cyclomatic_complexity = db.Column(db.Integer, default=0)
    time_complexity = db.Column(db.String(50))
    space_complexity = db.Column(db.String(50))
    
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        username = self.user.username if self.user else 'Anonymous'
        return f'<Submission {self.problem_title} by {username}>'

class LearningPath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Path details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty_level = db.Column(db.String(20))
    estimated_duration = db.Column(db.Integer)  # in hours
    
    # Progress tracking
    current_step = db.Column(db.Integer, default=0)
    total_steps = db.Column(db.Integer, default=0)
    completion_percentage = db.Column(db.Float, default=0.0)
    
    # Content
    learning_modules = db.Column(db.Text)  # JSON string of modules
    recommended_problems = db.Column(db.Text)  # JSON string of problems
    resources = db.Column(db.Text)  # JSON string of resources
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LearningPath {self.title} for {self.user.username}>'

class KnowledgeGap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Gap details
    concept = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # algorithms, data_structures, patterns, etc.
    severity = db.Column(db.String(20))  # low, medium, high, critical
    
    # Identified from
    identified_from_submission = db.Column(db.Integer, db.ForeignKey('submission.id'))
    confidence_score = db.Column(db.Float, default=0.0)
    
    # Status
    status = db.Column(db.String(20), default='identified')  # identified, learning, mastered
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<KnowledgeGap {self.concept} for {self.user.username}>'

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # article, video, tutorial, problem, book
    url = db.Column(db.String(500))
    description = db.Column(db.Text)
    
    # Categorization
    concepts = db.Column(db.Text)  # JSON string of concepts covered
    difficulty_level = db.Column(db.String(20))
    language = db.Column(db.String(50))
    
    # Ratings
    rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Resource {self.title}>'

class ProgressMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Metrics
    metric_name = db.Column(db.String(100), nullable=False)
    metric_value = db.Column(db.Float, nullable=False)
    metric_type = db.Column(db.String(50))  # score, time, count, percentage
    
    # Context
    context = db.Column(db.Text)  # JSON string with additional context
    
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProgressMetric {self.metric_name}: {self.metric_value}>'
