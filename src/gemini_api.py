import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'


def call_gemini(prompt, temperature=0.2, max_tokens=1024):
    """
    Call Gemini 2.0 Flash API with the given prompt and return the response.
    """
    if not GEMINI_API_KEY:
        raise ValueError('GEMINI_API_KEY is not set in the environment.')

    headers = {
        'Content-Type': 'application/json',
    }
    params = {
        'key': GEMINI_API_KEY
    }
    data = {
        'contents': [{
            'parts': [{
                'text': prompt
            }]
        }],
        'generationConfig': {
            'temperature': temperature,
            'maxOutputTokens': max_tokens
        }
    }
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    response.raise_for_status()
    result = response.json()
    # Extract the generated text from the response
    try:
        return result['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        return result
