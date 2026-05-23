// repair-check.ts — flag dialog nodes missing required repair transitions
// Run: npx ts-node repair-check.ts <flow.json>

type Node = {
  id: string;
  class?: "open" | "directed" | "option" | "confirm";
  destructive?: boolean;
  transitions: { trigger: string; to: string }[];
};

type FlowFile = { nodes: Node[] };

const REQUIRED_TRIGGERS = ["no-match", "no-input", "max-retry"];

export function lintFlow(nodes: Node[]): { node_id: string; defect: string }[] {
  const issues: { node_id: string; defect: string }[] = [];

  for (const n of nodes) {
    // Escalation nodes are terminal — skip them
    if (n.id.includes("escalate")) continue;

    const triggers = new Set(n.transitions.map((t) => t.trigger));

    for (const required of REQUIRED_TRIGGERS) {
      if (!triggers.has(required)) {
        issues.push({ node_id: n.id, defect: `missing:${required}` });
      }
    }

    if (n.destructive && !triggers.has("explicit-confirm")) {
      issues.push({ node_id: n.id, defect: "destructive-without-explicit-confirm" });
    }
  }

  return issues;
}

// CLI entry point
import * as fs from "fs";
const file: FlowFile = JSON.parse(fs.readFileSync(process.argv[2], "utf-8"));
const issues = lintFlow(file.nodes);
if (issues.length === 0) {
  console.log("OK: all nodes have required repair transitions");
  process.exit(0);
} else {
  for (const i of issues) console.error(`FAIL: ${i.node_id} — ${i.defect}`);
  process.exit(1);
}
