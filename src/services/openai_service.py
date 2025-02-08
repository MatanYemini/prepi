import json
import base64
import websockets
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect
import asyncio

from config.settings import LOG_EVENT_TYPES, OPENAI_API_KEY, VOICE, SYSTEM_MESSAGE, SHOW_TIMING_MATH, MAX_CALL_DURATION
from utils.websocket_handlers import WebSocketState, handle_speech_started_event, send_mark

async def initialize_session(openai_ws):
    """Control initial session with OpenAI."""
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": VOICE,
            "instructions": SYSTEM_MESSAGE,
            "modalities": ["text", "audio"],
            "temperature": 0.8,
        }
    }
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))
    await send_initial_conversation_item(openai_ws)

async def send_initial_conversation_item(openai_ws):
    """Send initial conversation item if AI talks first."""
    initial_conversation_item = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Greet the user with: 'Hey there! I hope you're having an amazing day! I just wanted to check in and see if there's anything I can do to help you'"
                }
            ]
        }
    }
    await openai_ws.send(json.dumps(initial_conversation_item))
    await openai_ws.send(json.dumps({"type": "response.create"}))

async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections between Twilio and OpenAI."""
    print("Client connected")
    await websocket.accept()

    async with websockets.connect(
        'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01',
        extra_headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
    ) as openai_ws:
        await initialize_session(openai_ws)
        
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