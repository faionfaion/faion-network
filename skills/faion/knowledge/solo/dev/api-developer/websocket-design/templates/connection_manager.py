"""
FastAPI WebSocket ConnectionManager with channel subscriptions.
Handles connect/disconnect, channel subscribe/unsubscribe, and broadcast.
For horizontal scaling, replace broadcast_to_channel with Redis Pub/Sub.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import asyncio
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.channel_subscriptions: Dict[str, Set[str]] = {}
        self.user_channels: Dict[str, Set[str]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        # Disconnect existing connection for same user (session takeover)
        if user_id in self.active_connections:
            await self.disconnect(user_id)
        self.active_connections[user_id] = websocket
        self.user_channels[user_id] = set()

    async def disconnect(self, user_id: str):
        if user_id not in self.active_connections:
            return
        for channel in list(self.user_channels.get(user_id, [])):
            self._unsubscribe(user_id, channel)
        ws = self.active_connections.pop(user_id, None)
        self.user_channels.pop(user_id, None)
        if ws:
            try:
                await ws.close()
            except Exception:
                pass

    def _unsubscribe(self, user_id: str, channel: str):
        self.channel_subscriptions.get(channel, set()).discard(user_id)
        self.user_channels.get(user_id, set()).discard(channel)

    async def subscribe(self, user_id: str, channel: str):
        self.channel_subscriptions.setdefault(channel, set()).add(user_id)
        self.user_channels.setdefault(user_id, set()).add(channel)

    async def broadcast_to_channel(self, channel: str, message: dict):
        subscribers = list(self.channel_subscriptions.get(channel, set()))
        await asyncio.gather(
            *[self.send_to_user(uid, message) for uid in subscribers],
            return_exceptions=True,
        )

    async def send_to_user(self, user_id: str, message: dict):
        ws = self.active_connections.get(user_id)
        if ws:
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                await self.disconnect(user_id)


app = FastAPI()
manager = ConnectionManager()


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    # TODO: authenticate user_id via ticket or cookie before accepting
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            msg_type = message.get("type")

            if msg_type == "ping":
                await manager.send_to_user(user_id, {"type": "pong"})
            elif msg_type == "subscribe":
                channel = message.get("channel")
                if channel:
                    await manager.subscribe(user_id, channel)
            elif msg_type == "message":
                channel = message.get("channel")
                if channel:
                    await manager.broadcast_to_channel(channel, message)
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
