// __faion_header_v1__
// purpose: TypeScript WebSocketClient: reconnect with exponential jitter, offline queue, heartbeat
// consumes: see content/02-output-contract.xml
// produces: spec; depends-on: content/01-core-rules.xml#versioned-envelope
// faion_header_json: {"__faion_header__":{"purpose":"TypeScript WebSocketClient: reconnect with exponential jitter, offline queue, heartbeat","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#versioned-envelope","token_budget_impact":"~150 tokens when loaded"}}
type Msg = { v: number; type: string; channel: string; seq: number; ts: number; payload: unknown };

export class WSClient {
  private ws?: WebSocket;
  private attempts = 0;
  private queue: Msg[] = [];
  private readonly maxQueue = 100;
  private readonly url: string;
  private heartbeat?: ReturnType<typeof setInterval>;

  constructor(url: string) { this.url = url; this.connect(); }

  private connect() {
    this.ws = new WebSocket(this.url);
    this.ws.onopen = () => { this.attempts = 0; this.flush(); this.startHeartbeat(); };
    this.ws.onclose = () => { this.stopHeartbeat(); this.scheduleReconnect(); };
    this.ws.onmessage = (e) => this.handle(JSON.parse(e.data));
  }

  private scheduleReconnect() {
    if (this.attempts > 8) return;
    const cap = 30_000, base = 1000;
    const delay = Math.random() * Math.min(cap, base * Math.pow(2, this.attempts));
    this.attempts += 1;
    setTimeout(() => this.connect(), delay);
  }

  private startHeartbeat() { this.heartbeat = setInterval(() => this.send({ type: 'ping' } as Msg), 25_000); }
  private stopHeartbeat() { if (this.heartbeat) clearInterval(this.heartbeat); }
  private flush() { while (this.queue.length && this.ws?.readyState === 1) this.ws.send(JSON.stringify(this.queue.shift())); }
  private handle(_m: Msg) { /* delegate to listeners */ }
  send(m: Msg) {
    if (this.queue.length >= this.maxQueue) this.queue.shift();
    this.queue.push(m); this.flush();
  }
}
