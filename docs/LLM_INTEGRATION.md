# LLM Integration Guide

## Overview

The Coding Learning Recommender now includes powerful LLM (Large Language Model) integration using Google's Gemini 2.0 Flash model. This enhancement provides deep code understanding, educational insights, and comprehensive explanations that go beyond traditional static analysis.

## Features

### Enhanced Code Analysis
- **Deep Algorithm Understanding**: Explains the algorithm used and its purpose
- **Optimization Suggestions**: Provides specific recommendations for improvement
- **Learning Concepts**: Identifies key concepts students should understand
- **Alternative Approaches**: Suggests different ways to solve the problem
- **Code Quality Feedback**: Detailed feedback on style and structure
- **Interview Tips**: Guidance for technical interviews
- **Related Problems**: Suggestions for similar practice problems

### Educational Insights
- **Conceptual Gap Analysis**: Identifies missing knowledge areas
- **Positive Reinforcement**: Highlights what the student did well
- **Complexity Explanations**: Detailed reasoning for time/space complexity
- **Best Practices**: Coding standards and conventions guidance

## Setup

### 1. Install Dependencies

The required dependency is already included in `requirements.txt`:

```bash
pip install google-generativeai>=0.3.0
```

### 2. Configure API Key

Add your Gemini API key to the `.env` file:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

To get a Gemini API key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### 3. Verify Integration

Run the test script to verify everything is working:

```bash
python test_llm_integration.py
```

## Usage

### API Endpoints

#### Enhanced Analysis
```http
POST /api/analyze-enhanced
Content-Type: application/json

{
    "user_id": 1,
    "code": "def two_sum(nums, target): ...",
    "language": "python",
    "problem_title": "Two Sum"
}
```

**Response:**
```json
{
    "analysis": {
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "patterns": ["hash_table"],
        "llm_analysis": {
            "algorithm_explanation": "...",
            "optimization_suggestions": [...],
            "learning_concepts": [...],
            "interview_tips": [...]
        }
    },
    "educational_summary": "🎯 **Algorithm Analysis:** ...",
    "recommendations": {...},
    "llm_enabled": true
}
```

#### Code Explanation
```http
POST /api/explain-code
Content-Type: application/json

{
    "code": "def binary_search(arr, target): ...",
    "language": "python"
}
```

**Response:**
```json
{
    "explanation": "🎯 **Algorithm Analysis:** ...",
    "llm_enabled": true
}
```

### Python Integration

```python
from src.llm_enhanced_analyzer import LLMEnhancedAnalyzer

# Initialize the analyzer
analyzer = LLMEnhancedAnalyzer()

# Analyze code with LLM enhancement
code = "def fibonacci(n): ..."
analysis = analyzer.analyze_code_with_llm(code, "python")

# Get educational summary
summary = analyzer.get_educational_summary(analysis)
print(summary)

# Quick explanation
explanation = analyzer.analyze_and_explain(code, "python")
print(explanation)
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes (for LLM features) |
| `CODE_ANALYSIS_TIMEOUT` | Analysis timeout in seconds | No (default: 30) |
| `MAX_CODE_LENGTH` | Maximum code length | No (default: 10,000) |

### Model Configuration

The system uses Gemini 2.0 Flash with these settings:
- **Max Output Tokens**: 1,500
- **Temperature**: 0.3 (for consistent, focused responses)
- **Model**: `gemini-2.0-flash`

## Fallback Behavior

If the Gemini API key is not configured or the API is unavailable:
- The system automatically falls back to traditional analysis
- All endpoints continue to work normally
- `llm_enabled` field in responses will be `false`
- Educational summaries will indicate "No LLM analysis available"

## Example Outputs

### Traditional vs Enhanced Analysis

**Traditional Analysis:**
```json
{
    "time_complexity": "O(n)",
    "space_complexity": "O(n)",
    "patterns": ["hash_table"],
    "quality_score": 85.0
}
```

**Enhanced Analysis:**
```json
{
    "time_complexity": "O(n)",
    "space_complexity": "O(n)",
    "patterns": ["hash_table"],
    "quality_score": 85.0,
    "llm_analysis": {
        "algorithm_explanation": "This implements an efficient two-sum solution using a hash table to achieve O(n) time complexity...",
        "optimization_suggestions": [
            "Consider adding input validation for edge cases",
            "Add type hints for better code documentation"
        ],
        "learning_concepts": [
            "Hash table time complexity",
            "Space-time tradeoffs",
            "One-pass algorithms"
        ],
        "interview_tips": [
            "Explain the hash table approach clearly",
            "Discuss why this is better than brute force"
        ]
    }
}
```

### Educational Summary Example

```markdown
🎯 **Algorithm Analysis:**
   This implements an efficient two-sum solution using a hash table to achieve O(n) time complexity. The algorithm makes a single pass through the array while maintaining a lookup table of previously seen values.

✅ **What you did well:**
   • Chose an optimal O(n) solution over brute force O(n²)
   • Used clear variable names (complement, seen)
   • Handled the return case correctly

🚀 **Optimization suggestions:**
   • Consider adding input validation for edge cases
   • Add type hints for better code documentation
   • Consider handling duplicate values explicitly

📚 **Key concepts to understand:**
   • Hash table time complexity and space tradeoffs
   • One-pass algorithm design
   • Complement calculation technique

💼 **Interview tips:**
   • Explain why hash table is better than brute force
   • Discuss space-time tradeoffs
   • Walk through the algorithm step by step
```

## Best Practices

### 1. Error Handling
Always check if LLM is enabled before relying on LLM-specific features:

```python
if analyzer.use_llm:
    # Use enhanced features
    analysis = analyzer.analyze_code_with_llm(code, language)
else:
    # Fall back to traditional analysis
    analysis = analyzer.analyze_code(code, language)
```

### 2. Rate Limiting
Be mindful of API rate limits when making frequent requests:
- Implement caching for repeated analyses
- Consider batching requests when possible
- Monitor API usage and costs

### 3. Content Filtering
The system includes basic content filtering, but always validate:
- Code length limits
- Language support
- Malicious code detection

## Troubleshooting

### Common Issues

1. **"Gemini API key not found"**
   - Check `.env` file has `GEMINI_API_KEY` set
   - Verify the key is valid and active

2. **"Failed to parse LLM response as JSON"**
   - Usually temporary API issues
   - The system will fall back gracefully
   - Check API status and retry

3. **"Gemini analysis failed"**
   - Network connectivity issues
   - API rate limit exceeded
   - Invalid API key

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

analyzer = LLMEnhancedAnalyzer()
# Debug information will be printed
```

## Performance Considerations

### Response Times
- Traditional analysis: ~100-500ms
- LLM-enhanced analysis: ~2-5 seconds
- Consider async processing for better UX

### Caching
Implement caching for:
- Repeated code submissions
- Common algorithm patterns
- Educational content

### Cost Management
- Monitor API usage through Google Cloud Console
- Implement request quotas per user
- Cache responses when appropriate

## Future Enhancements

### Planned Features
- **Multi-language LLM Support**: Enhanced analysis for Java, C++, JavaScript
- **Custom Prompts**: Configurable analysis prompts for different use cases
- **Batch Processing**: Analyze multiple submissions efficiently
- **Learning Path Integration**: LLM-generated personalized learning paths
- **Code Review Mode**: Detailed code review with suggestions
- **Interview Simulation**: Mock interview scenarios with LLM feedback

### Integration Opportunities
- **IDE Plugins**: Real-time code analysis in popular IDEs
- **GitHub Integration**: Automated code review for repositories
- **Learning Platforms**: Integration with educational platforms
- **Competitive Programming**: Contest-specific analysis and tips

## Support

For LLM integration issues:
1. Check the troubleshooting section above
2. Verify API key configuration
3. Test with the provided example scripts
4. Create an issue on GitHub with detailed error information

## References

- [Google Generative AI Documentation](https://ai.google.dev/docs)
- [Gemini API Reference](https://ai.google.dev/api/rest)
- [Google AI Studio](https://makersuite.google.com/)