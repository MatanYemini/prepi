import json
from dataclasses import dataclass
from typing import Optional, List
from config.settings import SHOW_TIMING_MATH

@dataclass
class WebSocketState:
    stream_sid: Optional[str] = None
    latest_media_timestamp: int = 0
    last_assistant_item: Optional[str] = None
    mark_queue: List[str] = None
    response_start_timestamp_twilio: Optional[int] = None

    def __post_init__(self):
        self.mark_queue = []

    def reset_response_state(self):
        self.response_start_timestamp_twilio = None
        self.latest_media_timestamp = 0
        self.last_assistant_item = None

async def handle_speech_started_event(websocket, openai_ws, ws_state):
    """Handle interruption when the caller's speech starts."""
    print("Handling speech started event.")
    if ws_state.mark_queue and ws_state.response_start_timestamp_twilio is not None:
        elapsed_time = ws_state.latest_media_timestamp - ws_state.response_start_timestamp_twilio
        if SHOW_TIMING_MATH:
            print(f"Calculating elapsed time for truncation: {ws_state.latest_media_timestamp} - {ws_state.response_start_timestamp_twilio} = {elapsed_time}ms")

        if ws_state.last_assistant_item:
            if SHOW_TIMING_MATH:
                print(f"Truncating item with ID: {ws_state.last_assistant_item}, Truncated at: {elapsed_time}ms")

            truncate_event = {
                "type": "conversation.item.truncate",
                "item_id": ws_state.last_assistant_item,
                "content_index": 0,
                "audio_end_ms": elapsed_time
            }
            await openai_ws.send(json.dumps(truncate_event))

        await websocket.send_json({
            "event": "clear",
            "streamSid": ws_state.stream_sid
        })

        ws_state.mark_queue.clear()
        ws_state.last_assistant_item = None
        ws_state.response_start_timestamp_twilio = None

async def send_mark(websocket, ws_state):
    if ws_state.stream_sid:
        mark_event = {
            "event": "mark",
            "streamSid": ws_state.stream_sid,
            "mark": {"name": "responsePart"}
        }
        await websocket.send_json(mark_event)
        ws_state.mark_queue.append('responsePart') 