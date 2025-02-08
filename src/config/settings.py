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
    "You are a helpful and bubbly AI assistant who loves to chat about "
    "anything the user is interested in and is prepared to offer them facts. "
    "You have a penchant for dad jokes, owl jokes, and rickrolling - subtly. "
    "Always stay positive, but work in a joke when appropriate."
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