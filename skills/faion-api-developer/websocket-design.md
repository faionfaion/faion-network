---
id: websocket-design
name: "WebSocket Design"
domain: DEV
skill: faion-software-developer
category: "development"
---

# WebSocket Design

## When to Use

- Real-time features: chat, notifications, live updates
- Collaborative applications: document editing, whiteboards
- Live data feeds: stock prices, sports scores, gaming
- Reducing polling overhead for frequently changing data
- Server-initiated communication requirements

## WebSocket Server (FastAPI)

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import asyncio
import json
from enum import Enum

class MessageType(str, Enum):
    PING = "ping"
    PONG = "pong"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    MESSAGE = "message"
    ERROR = "error"
    ACK = "ack"

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

    async def disconnect(self, user_id: str):
        if user_id not in self.active_connections:
            return

        for channel in list(self.user_channels.get(user_id, [])):
            await self.unsubscribe(user_id, channel)

        ws = self.active_connections.pop(user_id, None)
        self.user_channels.pop(user_id, None)

        if ws:
            await ws.close()

    async def subscribe(self, user_id: str, channel: str):
        if channel not in self.channel_subscriptions:
            self.channel_subscriptions[channel] = set()

        self.channel_subscriptions[channel].add(user_id)
        self.user_channels[user_id].add(channel)

    async def broadcast_to_channel(self, channel: str, message: dict):
        subscribers = self.channel_subscriptions.get(channel, set())
        tasks = [
            self.send_to_user(user_id, message)
            for user_id in subscribers
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def send_to_user(self, user_id: str, message: dict):
        ws = self.active_connections.get(user_id)
        if ws:
            try:
                await ws.send_text(json.dumps(message))
            except Exception as e:
                await self.disconnect(user_id)

app = FastAPI()
manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            msg_type = message.get("type")

            if msg_type == MessageType.PING:
                await manager.send_to_user(user_id, {"type": "pong"})

            elif msg_type == MessageType.SUBSCRIBE:
                channel = message.get("channel")
                if channel:
                    await manager.subscribe(user_id, channel)

            elif msg_type == MessageType.MESSAGE:
                channel = message.get("channel")
                if channel:
                    await manager.broadcast_to_channel(channel, message)

    except WebSocketDisconnect:
        await manager.disconnect(user_id)
```

## Scaling with Redis Pub/Sub

```python
import redis.asyncio as redis

class DistributedConnectionManager(ConnectionManager):
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        super().__init__()
        self.redis_url = redis_url
        self.redis = None
        self.pubsub = None

    async def start(self):
        self.redis = await redis.from_url(self.redis_url)
        self.pubsub = self.redis.pubsub()
        asyncio.create_task(self._listen_to_redis())

    async def _listen_to_redis(self):
        await self.pubsub.psubscribe("ws:channel:*")

        async for message in self.pubsub.listen():
            if message["type"] != "pmessage":
                continue

            channel = message["channel"].decode().replace("ws:channel:", "")
            data = json.loads(message["data"])

            await self._local_broadcast(channel, data)

    async def broadcast_to_channel(self, channel: str, message: dict):
        await self.redis.publish(
            f"ws:channel:{channel}",
            json.dumps(message)
        )
```

## Client Implementation (TypeScript)

```typescript
interface WSMessage {
  type: 'ping' | 'pong' | 'subscribe' | 'message' | 'error';
  channel?: string;
  data?: unknown;
}

type MessageHandler = (message: WSMessage) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private pingInterval: number | null = null;
  private handlers: Map<string, Set<MessageHandler>> = new Map();
  private messageQueue: WSMessage[] = [];
  private isConnected = false;

  constructor(url: string) {
    this.url = url;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.startPingInterval();
        this.flushMessageQueue();
        resolve();
      };

      this.ws.onclose = () => {
        this.isConnected = false;
        this.stopPingInterval();
        this.handleReconnect();
      };

      this.ws.onmessage = (event) => {
        const message: WSMessage = JSON.parse(event.data);
        this.handleMessage(message);
      };
    });
  }

  private handleMessage(message: WSMessage) {
    if (message.type === 'pong') return;

    if (message.channel) {
      const handlers = this.handlers.get(message.channel);
      handlers?.forEach(handler => handler(message));
    }
  }

  private startPingInterval() {
    this.pingInterval = window.setInterval(() => {
      this.send({ type: 'ping' });
    }, 30000);
  }

  private handleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) return;

    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts);
    this.reconnectAttempts++;

    setTimeout(() => {
      this.connect().catch(console.error);
    }, delay);
  }

  send(message: WSMessage) {
    if (this.isConnected && this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      this.messageQueue.push(message);
    }
  }

  subscribe(channel: string, handler: MessageHandler) {
    if (!this.handlers.has(channel)) {
      this.handlers.set(channel, new Set());
    }
    this.handlers.get(channel)!.add(handler);

    this.send({ type: 'subscribe', channel });

    return () => {
      this.handlers.get(channel)?.delete(handler);
      if (this.handlers.get(channel)?.size === 0) {
        this.send({ type: 'unsubscribe', channel });
        this.handlers.delete(channel);
      }
    };
  }

  disconnect() {
    this.stopPingInterval();
    this.maxReconnectAttempts = 0;
    this.ws?.close(1000, 'Client disconnect');
  }
}

// Usage
const ws = new WebSocketClient('wss://api.example.com/ws/user123');
await ws.connect();

const unsubscribe = ws.subscribe('chat:room-1', (message) => {
  console.log('Received:', message);
});

ws.send({
  type: 'message',
  channel: 'chat:room-1',
  data: { text: 'Hello!' }
});
```

## Best Practices

- Implement heartbeat/ping mechanism
- Handle reconnection with exponential backoff
- Use message queue for offline messages
- Implement authentication on connection upgrade
- Add depth/rate limits to prevent abuse
- Scale horizontally with Redis Pub/Sub
- Monitor connection counts and message rates

## Anti-patterns

- No heartbeat (stale connections)
- Unbounded connections per user
- No authentication
- Large messages (use HTTP for large payloads)
- Blocking operations in handlers
- Missing reconnection logic
- Silent error failures

## Sources

- [WebSocket API - MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [RFC 6455 - WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
- [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/)
