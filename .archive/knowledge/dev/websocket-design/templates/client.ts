// purpose: Client reconnect + heartbeat skeleton with exponential backoff + full jitter.
// consumes: see content/02-output-contract.xml inputs for websocket-design
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
type State = 'closed' | 'connecting' | 'open';

export class WSClient {
  private state: State = 'closed';
  private socket: WebSocket | null = null;
  private attempt = 0;
  private pingTimer?: ReturnType<typeof setInterval>;
  constructor(private url: () => string) {}
  connect(): void {
    this.state = 'connecting';
    const socket = new WebSocket(this.url());
    this.socket = socket;
    socket.onopen = () => { this.state = 'open'; this.attempt = 0; this.startHeartbeat(); };
    socket.onclose = () => { this.state = 'closed'; this.stopHeartbeat(); this.scheduleReconnect(); };
    socket.onmessage = (e) => { /* dispatch */ };
  }
  private scheduleReconnect(): void {
    const base = Math.min(60000, 1000 * 2 ** this.attempt);
    const delay = Math.floor(Math.random() * base);
    this.attempt++;
    setTimeout(() => this.connect(), delay);
  }
  private startHeartbeat(): void {
    this.pingTimer = setInterval(() => this.socket?.send(JSON.stringify({ v: 1, type: 'ping', id: crypto.randomUUID(), ts: Date.now(), payload: {} })), 30000);
  }
  private stopHeartbeat(): void { if (this.pingTimer) clearInterval(this.pingTimer); }
}
