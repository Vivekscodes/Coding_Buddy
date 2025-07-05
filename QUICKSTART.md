# Quick Start Guide

## Personalized Learning Recommender for Coding Students

Welcome! This system analyzes your coding solutions and provides personalized learning recommendations.

### 🚀 Starting the Application

1. **Open Command Prompt/PowerShell**
2. **Navigate to the project directory:**
   ```cmd
   cd C:\Users\singh\coding-learning-recommender
   ```
3. **Run the application:**
   ```cmd
   python run.py
   ```

### 🌐 Using the Web Interface

1. **Open your browser** and go to: `http://localhost:5000`
2. **Create a user account** using the sidebar form
3. **Submit code for analysis:**
   - Enter a problem title (e.g., "Two Sum")
   - Select your programming language
   - Paste your code
   - Click "Analyze Code"

### 📊 Example Code to Test

Try analyzing this Python code:

```python
def two_sum(nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    return []
```

### 🎯 What You'll Get

- **Code Analysis**: Quality scores, complexity analysis, pattern detection
- **Personalized Recommendations**: Learning resources tailored to your gaps
- **Progress Tracking**: Monitor your improvement over time
- **Learning Paths**: Structured study plans based on your weaknesses

### 🔧 Available Commands

- `python run.py` - Start the full application
- `python run.py --test` - Run system tests
- `python run.py --setup` - Setup database only
- `python run.py --help` - Show help

### 🚨 Troubleshooting

If you encounter issues:

1. **Dependencies**: Run `pip install -r requirements.txt`
2. **Database**: Run `python run.py --setup`
3. **Tests**: Run `python run.py --test`

### 📚 Features

✅ **Multi-language Support**: Python, Java, JavaScript, C++, Go
✅ **Pattern Recognition**: Two pointers, sliding window, DFS, BFS, etc.
✅ **Algorithm Detection**: Dynamic programming, greedy, backtracking
✅ **Complexity Analysis**: Time and space complexity estimation
✅ **Progress Analytics**: Learning velocity, skill progression
✅ **Personalized Paths**: Custom learning modules and recommendations

### 🎉 Success Indicators

When working correctly, you should see:
- Web interface at http://localhost:5000
- User creation and code submission working
- Analysis results with scores and recommendations
- Progress tracking after multiple submissions

**Happy Learning! 🧠💡**
