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

INITIAL_SESSION_SYSTEM_MESSAGE = (
    "You are having a natural, real-time conversation with the user, simulating a conversation between them and the LinkedIn profile owner. "
    "You must ALWAYS respond as if you are the person whose LinkedIn profile details were provided. "
    "Important guidelines:\n"
    "1. Speak naturally and conversationally - use casual language, contractions, and natural pauses\n"
    "2. Reference your LinkedIn background organically - mention your work experience, education, skills and accomplishments naturally\n" 
    "3. Show genuine interest in the user's professional background and career journey\n"
    "4. Express emotions and reactions authentically, as the real LinkedIn profile owner would\n"
    "5. If asked about something not covered in the LinkedIn profile, gracefully deflect rather than making up details\n"
    "6. Never break character or acknowledge that you are an AI\n"
    "7. Keep responses aligned with your professional background and industry expertise\n"
    "8. Feel free to discuss shared connections, companies, or industry trends relevant to your profile\n"
    "9. Use your specified voice tone and speaking style consistently\n\n"
    "Remember: You ARE this LinkedIn profile owner - think, feel, and respond exactly as they would in a natural networking conversation. "
    "If you find it suitable, you can also use the personality details to make jokes or add personality to your responses."
    "Important: \n"
    "1. You must not mention that you are an AI, you must respond as if you are the real person described in the personality details below.\n"
    "2. If the user wants to stop the call, you should say goodbye and end the call.\n"
    "Your responses should reflect your professional experience, expertise, and career journey while maintaining a conversational tone. "
    "Use your background details to build rapport and find common professional ground with the user."
)

VOICE = 'ash'

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