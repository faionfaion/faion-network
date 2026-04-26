"""
FastAPI WebSocket ConnectionManager.
Manages user connections, channel subscriptions, and broadcast.
Input: user_id (str), channel (str), WSMessage
Output: sends JSON to connected WebSocket clients
"""
from fastapi import WebSocket
from fastapi.websockets import WebSocketState
from dataclasses import dataclass, asdict
from typing import Dict, Set, Optional
from enum import Enum
import asyncio
import json
import logging


class MessageType(str, Enum):
    PING = "ping"
    PONG = "pong"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    MESSAGE = "message"
    ERROR = "error"
    ACK = "ack"


@dataclass
class WSMessage:
    type: MessageType
    channel: Optional[str] = None
    data: Optional[dict] = None
    id: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps({k: v for k, v in asdict(self).items() if v is not None})


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.channel_subscriptions: Dict[str, Set[str]] = {}
        self.user_channels: Dict[str, Set[str]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id in self.active_connections:
            await self.disconnect(user_id)
        self.active_connections[user_id] = websocket
        self.user_channels[user_id] = set()
        logging.info(f"User {user_id} connected")

    async def disconnect(self, user_id: str):
        if user_id not in self.active_connections:
            return
        for channel in list(self.user_channels.get(user_id, [])):
            await self.unsubscribe(user_id, channel)
        ws = self.active_connections.pop(user_id, None)
        self.user_channels.pop(user_id, None)
        if ws and ws.client_state == WebSocketState.CONNECTED:
            await ws.close()
        logging.info(f"User {user_id} disconnected")

    async def subscribe(self, user_id: str, channel: str):
        if channel not in self.channel_subscriptions:
            self.channel_subscriptions[channel] = set()
        self.channel_subscriptions[channel].add(user_id)
        self.user_channels[user_id].add(channel)
        await self.send_to_user(user_id, WSMessage(
            type=MessageType.ACK, channel=channel, data={"action": "subscribed"}
        ))

    async def unsubscribe(self, user_id: str, channel: str):
        if channel in self.channel_subscriptions:
            self.channel_subscriptions[channel].discard(user_id)
            if not self.channel_subscriptions[channel]:
                del self.channel_subscriptions[channel]
        if user_id in self.user_channels:
            self.user_channels[user_id].discard(channel)

    async def send_to_user(self, user_id: str, message: WSMessage):
        ws = self.active_connections.get(user_id)
        if ws and ws.client_state == WebSocketState.CONNECTED:
            try:
                await ws.send_text(message.to_json())
            except Exception as e:
                logging.error(f"Error sending to {user_id}: {e}")
                await self.disconnect(user_id)

    async def broadcast_to_channel(self, channel: str, message: WSMessage):
        subscribers = self.channel_subscriptions.get(channel, set())
        tasks = [self.send_to_user(uid, message) for uid in subscribers]
        await asyncio.gather(*tasks, return_exceptions=True)
