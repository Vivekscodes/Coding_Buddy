# Troubleshooting Guide

## ✅ Fixed: Database Schema Issue

The original error was due to a database constraint violation. This has been **RESOLVED** by:

1. **Updated database schema** - Made `user_id` nullable in the `Submission` model
2. **Database migration** - Ran migration script to update the schema
3. **Added error handling** - Graceful fallback when database operations fail

## 🚀 Current Status

- ✅ Database schema updated
- ✅ Anonymous submissions supported
- ✅ Error handling improved
- ✅ LLM integration working
- ✅ Frontend updated with validation features

## 🔧 How to Use

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open browser to:**
   ```
   http://127.0.0.1:5000
   ```

3. **Test with sample code:**
   - Paste any code in the text area
   - Select programming language
   - Add expected behavior (optional)
   - Click "Analyze Code" or "Validate Only"

## 🧪 Testing

Run the test script to verify everything works:
```bash
python test_integration_demo.py
```

## 🐛 Common Issues & Solutions

### 1. LLM Validation Not Working
**Symptoms:** Getting "LLM validation unavailable" messages

**Solutions:**
- Check if you have a valid Gemini API key in your `.env` file
- Ensure you have internet connectivity
- The system will fall back to basic analysis if LLM is unavailable

### 2. Database Errors
**Symptoms:** SQL constraint errors

**Solutions:**
- The database has been migrated to support anonymous submissions
- If you still see issues, run: `python migrate_database.py`

### 3. Module Import Errors
**Symptoms:** Import errors when starting the app

**Solutions:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that all files are in the correct directories

### 4. Frontend Not Loading Validation Results
**Symptoms:** Analysis works but validation section not showing

**Solutions:**
- Clear browser cache
- Check browser console for JavaScript errors
- Ensure the validation section is being populated by the API response

## 📋 API Endpoints

### Full Analysis (Recommended)
```bash
POST /api/analyze
{
    "code": "your code here",
    "language": "python",
    "problem_title": "Problem Name",
    "expected_behavior": "What should it do?"
}
```

### Validation Only
```bash
POST /api/validate
{
    "code": "your code here",
    "language": "python",
    "expected_behavior": "What should it do?"
}
```

## ⚙️ Configuration

Ensure your `.env` file contains:
```
GEMINI_API_KEY=your_actual_api_key_here
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///learning_recommender.db
```

## 🔍 Debug Mode

The application runs in debug mode by default, so you'll see detailed error messages in the console if anything goes wrong.

## 📞 Still Having Issues?

1. Check the console output when running `python app.py`
2. Look for any error messages in the browser's developer console
3. Try the test script: `python test_integration_demo.py`
4. Ensure all dependencies are properly installed

The integration is now robust and should handle errors gracefully while providing the enhanced LLM validation features!
