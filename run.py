#!/usr/bin/env python3
"""
Startup script for the Coding Learning Recommender System
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_environment():
    """Set up the environment and check dependencies"""
    print("🚀 Starting Coding Learning Recommender System...")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check required environment variables
    required_vars = ['SECRET_KEY', 'DATABASE_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        sys.exit(1)
    
    print("✅ Environment variables configured")
    
    # Check dependencies
    try:
        import flask
        import flask_sqlalchemy
        import sklearn
        import numpy
        import pandas
        print("✅ Core dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)

def initialize_database():
    """Initialize the database"""
    print("\n📊 Initializing database...")
    
    try:
        # Import from the main app.py file
        from app import app
        from models.database import db
        
        with app.app_context():
            db.create_all()
            print("✅ Database initialized successfully")
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

def run_tests():
    """Run basic system tests"""
    print("\n🧪 Running system tests...")
    
    try:
        from tests.test_basic import run_sample_analysis
        run_sample_analysis()
        print("✅ System tests passed")
    except Exception as e:
        print(f"❌ System tests failed: {e}")
        print("The system may still work, but there might be issues")

def start_application():
    """Start the Flask application"""
    print("\n🌐 Starting web application...")
    print("="*60)
    print("🎯 Application will be available at: http://localhost:5000")
    print("📚 Features available:")
    print("   • Code analysis and recommendations")
    print("   • Progress tracking and analytics")
    print("   • Personalized learning paths")
    print("   • Multi-language support (Python, Java, JS, C++, Go)")
    print("="*60)
    print("⚡ Starting server... (Press Ctrl+C to stop)")
    print()
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\U0001f44b Application stopped by user")
    except Exception as e:
        print(f"\u274c Application error: {e}")
        sys.exit(1)

def show_help():
    """Show help information"""
    print("""
Coding Learning Recommender System
=================================

Usage: python run.py [option]

Options:
  --help, -h     Show this help message
  --test         Run system tests only
  --setup        Setup and check environment only
  --dev          Run in development mode (default)

Examples:
  python run.py           # Start the application
  python run.py --test    # Run tests only
  python run.py --setup   # Check setup only

Features:
• Analyzes coding solutions for patterns and quality
• Provides personalized learning recommendations
• Tracks progress and learning velocity
• Generates custom learning paths
• Supports multiple programming languages

For more information, see README.md
""")

def main():
    """Main entry point"""
    # Parse command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h']:
            show_help()
            return
        elif arg == '--test':
            setup_environment()
            run_tests()
            return
        elif arg == '--setup':
            setup_environment()
            initialize_database()
            print("\n✅ Setup completed successfully!")
            return
        elif arg == '--dev':
            pass  # Default behavior
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for available options")
            return
    
    # Normal startup sequence
    setup_environment()
    initialize_database()
    run_tests()
    start_application()

if __name__ == '__main__':
    main()
