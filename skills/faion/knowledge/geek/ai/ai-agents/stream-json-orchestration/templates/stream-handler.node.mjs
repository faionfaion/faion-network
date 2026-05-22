// purpose: Node.js orchestrator consuming `claude -p --output-format stream-json` line by line
// consumes: same flags as the Python version (allowedTools, max-turns, budget cap)
// produces: same StreamJsonRunReport JSON shape
// depends-on: Node >= 18 (built-in child_process + readline only)
// token-budget-impact: ~350 tokens to render

import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { mkdir, rename, writeFile, open } from "node:fs/promises";

/**
 * @param {{
 *   taskPrompt: string,
 *   allowedTools: string[],
 *   maxTurns: number,
 *   budgetCapUsd: number,
 *   logDir: string,
 *   cliPath?: string,
 *   safetyPredicate?: (event: any) => boolean,
 * }} opts
 */
export async function runStreamHandler(opts) {
  if (!opts.allowedTools?.length) throw new Error("allowedTools cannot be empty");
  if (!opts.maxTurns || opts.maxTurns < 1) throw new Error("maxTurns must be >= 1");
  await mkdir(opts.logDir, { recursive: true });
  const startedAt = new Date().toISOString();
  const cliPath = opts.cliPath ?? "claude";
  const proc = spawn(cliPath, [
    "-p", opts.taskPrompt,
    "--output-format", "stream-json",
    "--include-partial-messages",
    "--allowedTools", opts.allowedTools.join(","),
    "--max-turns", String(opts.maxTurns),
  ], { stdio: ["ignore", "pipe", "pipe"] });

  const tmpLog = `${opts.logDir}/pending.jsonl`;
  const logHandle = await open(tmpLog, "w");
  const rl = createInterface({ input: proc.stdout });

  let eventsCount = 0;
  let totalCostUsd = 0;
  let sessionId = "";
  let killReason = null;
  let resultSubtype = "error_during_execution";

  for await (const rawLine of rl) {
    const line = rawLine.trim();
    if (!line) continue;
    await logHandle.write(line + "\n");
    eventsCount += 1;
    let event;
    try { event = JSON.parse(line); } catch { continue; }
    if (event.type === "system" && event.subtype === "init") sessionId = event.session_id ?? "";
    if (typeof event.total_cost_usd === "number") totalCostUsd = event.total_cost_usd;
    if (totalCostUsd > opts.budgetCapUsd) { killReason = "budget_cap"; proc.kill("SIGTERM"); break; }
    if (opts.safetyPredicate && !opts.safetyPredicate(event)) { killReason = "safety_veto"; proc.kill("SIGTERM"); break; }
    if (event.type === "result") { resultSubtype = event.subtype ?? "success"; break; }
  }
  await logHandle.close();
  const sid = sessionId || "unknown";
  const replayPath = `${opts.logDir}/${sid}.jsonl`;
  try { await rename(tmpLog, replayPath); } catch {}
  const endedAt = new Date().toISOString();
  return {
    session_id: sid,
    cli: "claude-code",
    started_at: startedAt,
    ended_at: endedAt,
    events_count: Math.max(eventsCount, 1),
    result_subtype: killReason ? "killed_by_orchestrator" : resultSubtype,
    total_cost_usd: Number(totalCostUsd.toFixed(6)),
    kill_reason: killReason,
    replay_path: `runs/${sid}.jsonl`,
    allowed_tools: [...opts.allowedTools],
    max_turns: opts.maxTurns,
  };
}

async function _smokeTest() {
  const report = await runStreamHandler({
    taskPrompt: "echo hi",
    allowedTools: ["Read"],
    maxTurns: 5,
    budgetCapUsd: 0.1,
    logDir: "/tmp/stream_handler_smoke_node",
    cliPath: "/bin/false",
  });
  if (report.max_turns !== 5) throw new Error("smoke test failed");
}

if (import.meta.url === `file://${process.argv[1]}`) {
  _smokeTest().catch((e) => { console.error(e); process.exit(1); });
}
