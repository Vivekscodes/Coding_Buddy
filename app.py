from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

from src.code_analyzer import CodeAnalyzer
from src.llm_enhanced_analyzer import LLMEnhancedAnalyzer
from src.recommendation_engine import RecommendationEngine
from src.progress_tracker import ProgressTracker
from src.enhanced_tracker import EnhancedLearningTracker
from models.database import db, User, Submission, LearningPath

# Import the validation tester from test_llm_integration
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_llm_integration import CodeValidationTester

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///learning_recommender.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

# Initialize components
code_analyzer = CodeAnalyzer()
llm_enhanced_analyzer = LLMEnhancedAnalyzer()
recommendation_engine = RecommendationEngine()
progress_tracker = ProgressTracker()
validation_tester = CodeValidationTester()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static-site')
def static_site():
    """Serve the enhanced static website with personality assessment"""
    return app.send_static_file('index.html')

@app.route('/personality')
def personality_assessment():
    """Serve the personality assessment page before main application"""
    return render_template('personality_enhanced_index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """Analyze submitted code and provide recommendations with personality-based insights"""
    data = request.json
    
    code = data.get('code')
    language = data.get('language')
    problem_title = data.get('problem_title')
    expected_behavior = data.get('expected_behavior', '')
    personality_type = data.get('personality_type')  # Get personality type from frontend
    personality_scores = data.get('personality_scores')  # Get personality scores if available
    
    if not all([code, language, problem_title]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Analyze the code with personality context if available
        if personality_type:
            analysis = llm_enhanced_analyzer.analyze_with_personality(
                code, language, personality_type, personality_scores
            )
        else:
            analysis = code_analyzer.analyze_code(code, language)
        
        # Perform LLM validation with personality context
        validation_results = validation_tester.validate_code_correctness(
            code, language, expected_behavior, personality_type
        )
        
        # Generate comprehensive report
        detailed_report = validation_tester.generate_detailed_report(validation_results, analysis)
        
        # Add personality-specific summary if available
        if personality_type and 'personality_insights' in analysis:
            personality_summary = llm_enhanced_analyzer.get_personality_summary(analysis)
            detailed_report += f"\n\n{personality_summary}"
        
        # Save submission to database (without user_id)
        try:
            submission = Submission(
                user_id=None,  # No user required for anonymous submissions
                problem_title=problem_title,
                code=code,
                language=language,
                complexity_score=analysis.get('complexity_score', 0),
                quality_score=analysis.get('quality_score', 0),
                patterns_used=','.join(analysis.get('patterns', [])),
                algorithms_identified=','.join(analysis.get('algorithms', [])),
                lines_of_code=len(code.split('\n')),
                time_complexity=analysis.get('time_complexity', 'Unknown'),
                space_complexity=analysis.get('space_complexity', 'Unknown'),
                submitted_at=datetime.utcnow()
            )
            db.session.add(submission)
            db.session.commit()
        except Exception as db_error:
            db.session.rollback()
            print(f"Database error: {db_error}")
            # Continue without saving to database
            submission = type('MockSubmission', (), {'id': 'temp'})()
        
        # Generate recommendations with personality context
        recommendations = recommendation_engine.generate_recommendations(None, analysis)
        
        # Add personality-specific recommendations if available
        if personality_type and 'personality_insights' in analysis:
            recommendations['personality_recommendations'] = analysis['personality_insights']
        
        return jsonify({
            'analysis': analysis,
            'recommendations': recommendations,
            'validation': validation_results,
            'detailed_report': detailed_report,
            'submission_id': submission.id,
            'personality_type': personality_type
        })
        
    except Exception as e:
        print(f"Analysis error: {e}")
        # Try to provide basic analysis if LLM fails
        try:
            basic_analysis = code_analyzer.analyze_code(code, language)
            return jsonify({
                'analysis': basic_analysis,
                'recommendations': {'error': 'LLM recommendations unavailable'},
                'validation': {
                    'is_correct': False,
                    'syntax_errors': [],
                    'logic_errors': ['LLM validation unavailable - basic analysis only'],
                    'runtime_errors': [],
                    'performance_issues': [],
                    'best_practice_violations': [],
                    'solutions': [],
                    'test_cases': [],
                    'overall_assessment': 'Unable to perform comprehensive validation. Please check your configuration.'
                },
                'detailed_report': 'LLM analysis failed, but basic code analysis completed successfully.',
                'submission_id': 'error',
                'personality_type': personality_type
            })
        except Exception as final_error:
            return jsonify({'error': f'Complete analysis failed: {str(final_error)}'}), 500

@app.route('/api/validate', methods=['POST'])
def validate_code():
    """Validate code for correctness and provide detailed error analysis"""
    data = request.json
    
    code = data.get('code')
    language = data.get('language')
    expected_behavior = data.get('expected_behavior', '')
    personality_type = data.get('personality_type')
    
    if not all([code, language]):
        return jsonify({'error': 'Code and language are required'}), 400
    
    try:
        # Perform detailed validation with personality context
        validation_results = validation_tester.validate_code_correctness(
            code, language, expected_behavior, personality_type
        )
        
        # Get analysis with personality context if available
        if personality_type:
            analysis = llm_enhanced_analyzer.analyze_with_personality(code, language, personality_type)
        else:
            analysis = code_analyzer.analyze_code(code, language)
        
        # Generate comprehensive report
        detailed_report = validation_tester.generate_detailed_report(validation_results, analysis)
        
        return jsonify({
            'validation': validation_results,
            'detailed_report': detailed_report,
            'analysis': analysis,
            'personality_type': personality_type
        })
        
    except Exception as e:
        print(f"Validation error: {e}")
        # Return basic error analysis if LLM validation fails
        try:
            analysis = code_analyzer.analyze_code(code, language)
            return jsonify({
                'validation': {
                    'is_correct': False,
                    'syntax_errors': [],
                    'logic_errors': ['Unable to perform LLM validation - using basic analysis only'],
                    'runtime_errors': [],
                    'performance_issues': [],
                    'best_practice_violations': [],
                    'solutions': [],
                    'test_cases': [],
                    'overall_assessment': 'LLM validation unavailable. Please check your API configuration.'
                },
                'detailed_report': 'LLM validation failed. Basic analysis completed successfully.',
                'analysis': analysis,
                'personality_type': personality_type
            })
        except Exception as fallback_error:
            return jsonify({'error': f'Analysis failed: {str(fallback_error)}'}), 500

@app.route('/api/assess-personality', methods=['POST'])
def assess_personality_from_code():
    """Assess personality traits from code style and approach"""
    data = request.json
    
    code = data.get('code')
    language = data.get('language')
    
    if not all([code, language]):
        return jsonify({'error': 'Code and language are required'}), 400
    
    try:
        # Assess personality from code
        personality_assessment = llm_enhanced_analyzer.assess_personality_from_code(code, language)
        
        return jsonify({
            'personality_assessment': personality_assessment,
            'success': True
        })
        
    except Exception as e:
        print(f"Personality assessment error: {e}")
        return jsonify({
            'error': f'Personality assessment failed: {str(e)}',
            'success': False
        }), 500

@app.route('/api/personality-types', methods=['GET'])
def get_personality_types():
    """Get all available personality types and their descriptions"""
    try:
        personality_types = llm_enhanced_analyzer.get_personality_types()
        return jsonify({
            'personality_types': personality_types,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': f'Failed to get personality types: {str(e)}',
            'success': False
        }), 500

@app.route('/api/user/<int:user_id>/progress')
def get_user_progress(user_id):
    """Get user's learning progress and analytics"""
    try:
        progress = progress_tracker.get_user_progress(user_id)
        return jsonify(progress)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/<int:user_id>/learning-path')
def get_learning_path(user_id):
    """Get personalized learning path for user"""
    try:
        learning_path = recommendation_engine.generate_learning_path(user_id)
        return jsonify(learning_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @app.route('/api/user', methods=['POST'])
# def create_user():
    # """Create a new user"""
    # data = request.json
    # username = data.get('username')
    # email = data.get('email')
    
    # if not username or not email:
    #     return jsonify({'error': 'Username and email are required'}), 400
    
    # try:
    #     user = User(username=username, email=email)
    #     db.session.add(user)
    #     db.session.commit()
        
    #     return jsonify({'user_id': user.id, 'username': user.username})
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

@app.route('/api/resources')
def get_learning_resources():
    """Get available learning resources"""
    resources = recommendation_engine.get_learning_resources()
    return jsonify(resources)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
