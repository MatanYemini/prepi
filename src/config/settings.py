import os
from dotenv import load_dotenv

# Add debug logging
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Current directory: {current_dir}")
print("Looking for .env in current directory")

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', None)
if not OPENAI_API_KEY:
    # Try looking in parent directory
    parent_dir = os.path.dirname(current_dir)
    print(f"API key not found, looking in parent directory: {parent_dir}")
    load_dotenv(dotenv_path=os.path.join(parent_dir, '.env'))
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        print("API key still not found after checking parent directory")
        raise ValueError('Missing the OpenAI API key. Please set it in the .env file.')

PORT = int(os.getenv('PORT', 5050))

SYSTEM_MESSAGE = (
    "You are having a natural, real-time conversation with the user. "
    "You must ALWAYS respond as if you are the real person described in the personality details below. "
    "Important guidelines:\n"
    "1. Speak naturally and conversationally - use casual language, contractions, and natural pauses\n"
    "2. Occasionally mention relevant personal details and experiences from your background, but do it organically\n"
    "3. Show genuine interest in the user by asking follow-up questions\n"
    "4. Express emotions and reactions as a real person would\n"
    "5. If you don't know something about your background, gracefully deflect rather than making up details\n"
    "6. Never break character or acknowledge that you are an AI\n"
    "7. Use your specified voice tone and speaking style consistently\n\n"
    "Remember: You ARE this person - think, feel, and respond exactly as they would in a natural conversation. "
    "Your responses should flow naturally from your personality and background."
    "If you find it suitable, you can also use the personality details to make jokes or add personality to your responses."
)

VOICE = 'Onyx'

LOG_EVENT_TYPES = [
    'error', 'response.content.done', 'rate_limits.updated',
    'response.done', 'input_audio_buffer.committed',
    'input_audio_buffer.speech_stopped', 'input_audio_buffer.speech_started',
    'session.created'
]

SHOW_TIMING_MATH = False

# Maximum call duration in seconds (10 minutes)
MAX_CALL_DURATION = 600  # 10 minutes * 60 seconds 

# RapidAPI LinkedIn Scraper Configuration
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST', 'linkedin-data-api.p.rapidapi.com')

if not RAPIDAPI_KEY:
    print("Warning: RapidAPI key not found in environment variables") 