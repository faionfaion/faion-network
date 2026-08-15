// purpose: TS WebSocket client wrapper: backoff reconnect + heartbeat + envelope.
// consumes: see content/02-output-contract.xml inputs for websocket-design
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
/**
 * TypeScript WebSocket client with reconnect, message queue, and heartbeat.
 * Usage: const ws = new WebSocketClient('wss://api.example.com/ws/user123');
 *        await ws.connect();
 *        const unsubscribe = ws.subscribe('chat:room-1', handler);
 */
interface WSMessage {
  type: 'ping' | 'pong' | 'subscribe' | 'unsubscribe' | 'message' | 'error' | 'ack';
  channel?: string;
  data?: unknown;
  id?: string;
}

type MessageHandler = (message: WSMessage) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private readonly maxReconnectAttempts = 5;
  private readonly reconnectDelay = 1000;
  private pingInterval: ReturnType<typeof setInterval> | null = null;
  private handlers = new Map<string, Set<MessageHandler>>();
  private messageQueue: WSMessage[] = [];
  private isConnected = false;

  constructor(private readonly url: string) {}

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.startPing();
        this.flushQueue();
        resolve();
      };

      this.ws.onclose = () => {
        this.isConnected = false;
        this.stopPing();
        this.handleReconnect();
      };

      this.ws.onerror = (err) => reject(err);

      this.ws.onmessage = (event) => {
        const msg: WSMessage = JSON.parse(event.data as string);
        if (msg.type === 'pong') return;
        if (msg.channel) this.handlers.get(msg.channel)?.forEach(h => h(msg));
        this.handlers.get('*')?.forEach(h => h(msg));
      };
    });
  }

  send(message: WSMessage) {
    if (this.isConnected && this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      this.messageQueue.push(message);
    }
  }

  subscribe(channel: string, handler: MessageHandler): () => void {
    if (!this.handlers.has(channel)) this.handlers.set(channel, new Set());
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
    this.stopPing();
    this.maxReconnectAttempts = 0 as never;
    this.ws?.close(1000, 'Client disconnect');
  }

  private startPing() {
    this.pingInterval = setInterval(() => this.send({ type: 'ping' }), 25000);
  }

  private stopPing() {
    if (this.pingInterval) { clearInterval(this.pingInterval); this.pingInterval = null; }
  }

  private handleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) return;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts) + Math.random() * 1000;
    this.reconnectAttempts++;
    setTimeout(() => this.connect().catch(console.error), delay);
  }

  private flushQueue() {
    while (this.messageQueue.length > 0) {
      const msg = this.messageQueue.shift();
      if (msg) this.send(msg);
    }
  }
}

export { WebSocketClient, WSMessage, MessageHandler };
