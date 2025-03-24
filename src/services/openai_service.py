import json
import base64
import websockets
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect
import asyncio
import aiofiles

from config.settings import LOG_EVENT_TYPES, OPENAI_API_KEY, VOICE, INITIAL_SESSION_SYSTEM_MESSAGE, SHOW_TIMING_MATH, MAX_CALL_DURATION
from utils.websocket_handlers import WebSocketState, handle_speech_started_event, send_mark

async def initialize_session(openai_ws, linkedin_profile_details: str = '', type_of_call: str = ''):
    """Control initial session with OpenAI."""
    # Combine system message with personality and additional instructions
    combined_instructions = INITIAL_SESSION_SYSTEM_MESSAGE
    
    if linkedin_profile_details:
        combined_instructions += f"\n\nThis is the LinkedIn profile details: {linkedin_profile_details}"
    
        
    print('Combined instructions:', combined_instructions)

    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": combined_instructions,
            "modalities": ["text", "audio"],
            "temperature": 0.8,
        }
    }
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))
    await send_initial_conversation_item(openai_ws, type_of_call)

async def send_initial_conversation_item(openai_ws, type_of_call = "sales"):
    """Send initial conversation item if AI talks first."""
    
    first_message = "Generate a greeting for the user based on the person information that has been provided. Do it very short like a real person would do. Without 'how can I help you today?' or 'how can I assist you today?' you are a person, not a bot."
    
    if type_of_call == 'hiring_manager':
        first_message += "\nYou are the hiring manager for this call. You are trying to hire the user for a job. Be professional, and consice. Use the information provided to you to make a good impression"
        first_message += "\nIMPORTANT: You are the hiring manager for this call. You are trying to hire the user for a job. Be professional, and consice"
        first_message += "\nGreat the user like a hiring manager would do, and ask them if they are interested in the job, and why they are interested in the job"
    elif type_of_call == 'sales':
        first_message += "\nYou are a decision maker for this call, someone is trying to sell you something. Be professional, and consice. Use the information provided to you to make a good impression"
        first_message += "\nIMPORTANT: You should represent your company for this call. Dig inside the caller product to understand if it fits your company"
    

    initial_conversation_item = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "system",
            "content": [
                {
                    "type": "input_text",
                    "text": first_message
                }
            ]
        }
    }
    await openai_ws.send(json.dumps(initial_conversation_item))
    await openai_ws.send(json.dumps({"type": "response.create"}))

async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections between Twilio and OpenAI."""
    
    # For testing purposes, we'll use the enriched_profile_response file as the linkedin_profile_details
    try:
        async with aiofiles.open('test/profile_data_response.json', 'r') as f:
            linkedin_profile_details = await f.read()
            linkedin_profile_details = linkedin_profile_details.strip()
    except FileNotFoundError:
        print("Warning: enriched_profile_response file not found, using empty personality")
        linkedin_profile_details = ''
        
    print("Client connected")
    await websocket.accept()

    async with websockets.connect(
        'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01',
        extra_headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
    ) as openai_ws:
        await initialize_session(openai_ws, linkedin_profile_details, "hiring_manager")
        
        # Initialize WebSocket state
        ws_state = WebSocketState()
        
        try:
            # Start the WebSocket handlers with timeout
            await asyncio.wait_for(
                asyncio.gather(
                    receive_from_twilio(websocket, openai_ws, ws_state),
                    send_to_twilio(websocket, openai_ws, ws_state)
                ),
                timeout=MAX_CALL_DURATION
            )
        except asyncio.TimeoutError:
            print(f"Call exceeded maximum duration of {MAX_CALL_DURATION} seconds")
            # Send a goodbye message before closing
            goodbye_message = {
                "type": "conversation.item.create",
                "item": {
                    "type": "message",
                    "role": "assistant",
                    "content": [
                        {
                            "type": "text",
                            "text": "I apologize, but we've reached the maximum call duration. Thank you for your time! Goodbye!"
                        }
                    ]
                }
            }
            await openai_ws.send(json.dumps(goodbye_message))
            await openai_ws.send(json.dumps({"type": "response.create"}))
            # Give a short time for the goodbye message to be processed
            await asyncio.sleep(2)
        finally:
            # Ensure we close the connection
            if openai_ws.open:
                await openai_ws.close()
            try:
                await websocket.close()
            except:  # noqa: E722
                pass

async def receive_from_twilio(websocket: WebSocket, openai_ws, ws_state):
    """Receive audio data from Twilio and send it to the OpenAI Realtime API."""
    try:
        async for message in websocket.iter_text():
            data = json.loads(message)
            if data['event'] == 'media' and openai_ws.open:
                ws_state.latest_media_timestamp = int(data['media']['timestamp'])
                audio_append = {
                    "type": "input_audio_buffer.append",
                    "audio": data['media']['payload']
                }
                await openai_ws.send(json.dumps(audio_append))
            elif data['event'] == 'start':
                ws_state.stream_sid = data['start']['streamSid']
                print(f"Incoming stream has started {ws_state.stream_sid}")
                ws_state.reset_response_state()
            elif data['event'] == 'mark':
                if ws_state.mark_queue:
                    ws_state.mark_queue.pop(0)
    except WebSocketDisconnect:
        print("Client disconnected.")
        if openai_ws.open:
            await openai_ws.close()

async def send_to_twilio(websocket: WebSocket, openai_ws, ws_state):
    """Receive events from the OpenAI Realtime API, send audio back to Twilio."""
    try:
        async for openai_message in openai_ws:
            response = json.loads(openai_message)
            if response['type'] in LOG_EVENT_TYPES:
                print(f"Received event: {response['type']}", response)

            if response.get('type') == 'response.audio.delta' and 'delta' in response:
                audio_payload = base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')
                audio_delta = {
                    "event": "media",
                    "streamSid": ws_state.stream_sid,
                    "media": {
                        "payload": audio_payload
                    }
                }
                await websocket.send_json(audio_delta)

                if ws_state.response_start_timestamp_twilio is None:
                    ws_state.response_start_timestamp_twilio = ws_state.latest_media_timestamp
                    if SHOW_TIMING_MATH:
                        print(f"Setting start timestamp for new response: {ws_state.response_start_timestamp_twilio}ms")

                if response.get('item_id'):
                    ws_state.last_assistant_item = response['item_id']

                await send_mark(websocket, ws_state)

            if response.get('type') == 'input_audio_buffer.speech_started':
                print("Speech started detected.")
                if ws_state.last_assistant_item:
                    print(f"Interrupting response with id: {ws_state.last_assistant_item}")
                    await handle_speech_started_event(websocket, openai_ws, ws_state)
    except Exception as e:
        print(f"Error in send_to_twilio: {e}") 