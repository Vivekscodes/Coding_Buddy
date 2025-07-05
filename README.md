# Personalized Learning Recommender for Coding Students

## Overview

This is an AI-powered learning coach that analyzes coding solutions and provides personalized learning recommendations for college students practicing on platforms like LeetCode. The system understands individual coding patterns, identifies knowledge gaps, and creates tailored learning paths with relevant resources.

## Features

### Core Features
- **Code Analysis**: Analyzes code quality, patterns, and problem-solving approaches
- **LLM-Enhanced Analysis**: Powered by Gemini 2.0 Flash for deep code understanding
- **Knowledge Gap Identification**: Identifies specific areas for improvement
- **Personalized Recommendations**: Suggests learning resources and study plans
- **Progress Tracking**: Monitors learning progress and adapts recommendations
- **Learning Path Generation**: Creates step-by-step improvement roadmaps
- **Educational Insights**: Comprehensive explanations and learning guidance

### Technical Features
- **Multi-language Support**: Python, Java, JavaScript, C++, Go
- **Pattern Recognition**: Detects coding patterns like two pointers, sliding window, etc.
- **Algorithm Detection**: Identifies algorithms like dynamic programming, DFS, BFS
- **Complexity Analysis**: Estimates time and space complexity
- **Performance Tracking**: Tracks improvement over time
- **Web Interface**: User-friendly web interface for code submission and analysis

## Architecture

### Components
1. **Code Analyzer** - Analyzes submitted code for patterns, algorithms, and quality
2. **Recommendation Engine** - Generates personalized learning recommendations
3. **Progress Tracker** - Monitors user progress and learning velocity
4. **Knowledge Graph** - Maps relationships between programming concepts
5. **Web Interface** - Frontend for user interaction

### Technology Stack
- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with SQLite (easily switchable to PostgreSQL)
- **ML/AI**: scikit-learn, NumPy, pandas
- **LLM Integration**: Google Generative AI (Gemini 2.0 Flash)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Code Analysis**: Python AST, regex patterns, LLM-powered insights

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd coding-learning-recommender
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\\Scripts\\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env` (or use the existing `.env` file)
   - Add your Gemini API key for LLM features:
     ```env
     GEMINI_API_KEY=your-gemini-api-key-here
     ```
   - Update other configuration as needed

5. **Initialize the database**:
   ```bash
   python app.py
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

7. **Access the application**:
   - Open your browser and go to `http://localhost:5000`

## Usage

### Getting Started

1. **Create a User Account**:
   - Fill in username and email in the sidebar
   - Click "Create User"

2. **Submit Code for Analysis**:
   - Enter the problem title
   - Select programming language
   - Paste your code
   - Click "Analyze Code"

3. **View Analysis Results**:
   - Review code quality and complexity scores
   - Check detected patterns and algorithms
   - Read personalized recommendations

4. **Track Progress**:
   - Click "View Progress" to see detailed analytics
   - Monitor your learning velocity and trends

5. **Follow Learning Path**:
   - Click "Learning Path" to see personalized modules
   - Follow recommended study sequence

### Example Code Submission

```python
# Example: Two Sum Problem
def two_sum(nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    return []
```

This will be analyzed for:
- Data structures used (hash table)
- Patterns (hash table lookup)
- Time complexity (O(n))
- Space complexity (O(n))
- Code quality metrics

## API Endpoints

### User Management
- `POST /api/user` - Create new user
- `GET /api/user/<id>/progress` - Get user progress
- `GET /api/user/<id>/learning-path` - Get learning path

### Code Analysis
- `POST /api/analyze` - Analyze submitted code (traditional analysis)
- `POST /api/analyze-enhanced` - Analyze code with LLM enhancement
- `POST /api/explain-code` - Get educational explanation of code

### Resources
- `GET /api/resources` - Get learning resources

## Configuration

### Environment Variables

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///learning_recommender.db
FLASK_ENV=development
FLASK_DEBUG=True

# LLM Integration
GEMINI_API_KEY=your-gemini-api-key-here
```

### Performance Settings
- `CODE_ANALYSIS_TIMEOUT`: Maximum time for code analysis (default: 30s)
- `MAX_CODE_LENGTH`: Maximum characters in submitted code (default: 10,000)

## Development

### Project Structure
```
coding-learning-recommender/
├── app/                    # Core application modules
│   ├── code_analyzer.py    # Code analysis engine
│   ├── recommendation_engine.py  # Recommendation system
│   └── progress_tracker.py # Progress tracking
├── models/                 # Database models
│   └── database.py         # SQLAlchemy models
├── templates/              # HTML templates
│   └── index.html          # Main web interface
├── static/                 # Static files (CSS, JS, images)
├── tests/                  # Test files
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Adding New Features

1. **New Analysis Patterns**:
   - Update `code_analyzer.py` pattern dictionaries
   - Add detection logic in `_detect_patterns()` method

2. **New Learning Resources**:
   - Update `_load_learning_resources()` in `recommendation_engine.py`
   - Add to database via admin interface

3. **New Metrics**:
   - Add to `progress_tracker.py`
   - Update database models if needed

### Testing

Run the test suite:
```bash
python -m pytest tests/
```

### Code Quality

The system analyzes code for:
- **Complexity**: Cyclomatic complexity, nesting depth
- **Patterns**: Common algorithmic patterns
- **Best Practices**: Naming conventions, function length
- **Performance**: Time and space complexity

## Supported Programming Languages

- **Python**: Full AST analysis, pattern detection
- **Java**: Basic pattern recognition
- **JavaScript**: Basic pattern recognition  
- **C++**: Basic pattern recognition
- **Go**: Basic pattern recognition

## Learning Path Examples

### Beginner Path
1. Array fundamentals
2. Basic string manipulation
3. Simple loops and conditionals
4. Hash table basics

### Intermediate Path
1. Two pointers technique
2. Sliding window pattern
3. Recursion and backtracking
4. Dynamic programming basics

### Advanced Path
1. Advanced DP patterns
2. Graph algorithms
3. System design concepts
4. Optimization techniques

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Enhancements

- **AI Integration**: LLM-powered code review and suggestions
- **Competitive Programming**: Support for contest platforms
- **Collaborative Learning**: Peer review and discussion features
- **Mobile App**: React Native mobile application
- **Video Tutorials**: Integrated video learning content
- **Gamification**: Badges, streaks, and achievements
- **Real-time Collaboration**: Live coding sessions
- **Interview Preparation**: Mock interview scenarios

## Support

For support, questions, or feature requests:
- Create an issue on GitHub
- Email: support@codinglearningrecommender.com
- Documentation: [Wiki](repository-url/wiki)

## Acknowledgments

- LeetCode for inspiration and problem examples
- scikit-learn community for ML algorithms
- Flask community for web framework
- Bootstrap for UI components
