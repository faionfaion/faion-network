/**
 * WebSocketClient with:
 * - Exponential backoff + full jitter reconnect
 * - Bounded offline message queue (max 100)
 * - Subscribe/unsubscribe with cleanup
 *
 * Usage:
 *   const client = new WebSocketClient('wss://api.example.com/ws/user123');
 *   await client.connect();
 *   const unsub = client.subscribe('chat:room-1', msg => console.log(msg));
 *   // cleanup
 *   unsub();
 *   client.disconnect();
 */
interface WSMessage {
  type: string;
  channel?: string;
  data?: unknown;
}
type MessageHandler = (message: WSMessage) => void;

const MAX_QUEUE = 100;
const MAX_RETRIES = 10;
const BASE_DELAY_MS = 500;
const CAP_DELAY_MS = 30_000;

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private pingInterval: ReturnType<typeof setInterval> | null = null;
  private handlers: Map<string, Set<MessageHandler>> = new Map();
  private messageQueue: WSMessage[] = [];
  private connected = false;

  constructor(private readonly url: string) {}

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.connected = true;
        this.reconnectAttempts = 0;
        this.startPing();
        this.flushQueue();
        resolve();
      };

      this.ws.onclose = () => {
        this.connected = false;
        this.stopPing();
        this.scheduleReconnect();
      };

      this.ws.onerror = (err) => {
        if (!this.connected) reject(err);
      };

      this.ws.onmessage = (ev) => {
        const msg: WSMessage = JSON.parse(ev.data as string);
        if (msg.type === 'pong') return;
        if (msg.channel) {
          this.handlers.get(msg.channel)?.forEach(h => h(msg));
        }
      };
    });
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

  send(message: WSMessage): void {
    if (this.connected && this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      if (this.messageQueue.length >= MAX_QUEUE) this.messageQueue.shift();
      this.messageQueue.push(message);
    }
  }

  disconnect(): void {
    this.reconnectAttempts = MAX_RETRIES; // prevent further reconnects
    this.stopPing();
    this.ws?.close(1000, 'client-disconnect');
  }

  private startPing() {
    this.pingInterval = setInterval(() => this.send({ type: 'ping' }), 25_000);
  }

  private stopPing() {
    if (this.pingInterval !== null) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  private flushQueue() {
    while (this.messageQueue.length > 0) {
      const msg = this.messageQueue.shift()!;
      this.ws?.send(JSON.stringify(msg));
    }
  }

  private scheduleReconnect() {
    if (this.reconnectAttempts >= MAX_RETRIES) return;
    // Full jitter: uniform(0, min(cap, base * 2^n))
    const delay = Math.random() * Math.min(CAP_DELAY_MS, BASE_DELAY_MS * 2 ** this.reconnectAttempts);
    this.reconnectAttempts++;
    setTimeout(() => this.connect().catch(() => {}), delay);
  }
}
