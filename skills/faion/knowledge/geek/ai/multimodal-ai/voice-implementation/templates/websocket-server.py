"""FastAPI WebSocket endpoint wiring ProductionVoiceAgent."""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from production_agent import ProductionVoiceAgent, VoiceAgentConfig

app = FastAPI()


@app.websocket("/voice")
async def voice_endpoint(websocket: WebSocket) -> None:
    """WebSocket voice endpoint. Receives audio bytes, returns audio bytes."""
    await websocket.accept()

    config = VoiceAgentConfig(
        system_prompt="You are a helpful voice assistant. Keep responses under 2 sentences.",
        voice="nova",
        max_response_tokens=150
    )
    agent = ProductionVoiceAgent(config)
    await agent.start_session()

    try:
        while True:
            audio_data = await websocket.receive_bytes()
            response_audio = await agent.handle_audio(audio_data)
            if response_audio:
                await websocket.send_bytes(response_audio)
    except WebSocketDisconnect:
        # Normal disconnect — no error logging
        pass
    except Exception as e:
        # Actual error — log separately from normal disconnect
        import logging
        logging.getLogger(__name__).error(f"WebSocket error: {e}")
    finally:
        await agent.end_session()
