# Faion Knowledge

**Entry Point:** `/faion`

Umbrella knowledge skill: 20 canonical domains, ~2628 methodologies (v3 layout). Tier-partitioned (free / solo / pro / geek). Two-level retrieval — read L1 first (`knowledge/domains.xml`), then drill into ≤3 L2 indexes (`knowledge/<domain>/INDEX.xml`) before opening any leaf.

## Canonical 20 domains (post-F-065 merge)

```
ai-core (82)     ai-agents (101)   ml-engineering (195)   sdlc-ai (89)
dev (374)        backend (161)     frontend (132)         architecture (59)
infra (293)      security (1)      claude-code (9)
pm (324)         product (75)      ba (118)               sdd (117)
ux (93)          research (87)
marketing (276)  comms (26)        hr (15)
```

## Retrieval flow (2-level)

1. Read `knowledge/domains.xml` (L1) — 20 domains + scope + decision-tree + disambiguation.
2. Pick ≤3 candidate domains via the decision-tree.
3. Read each picked `knowledge/<domain>/INDEX.xml` (L2) — methodologies partitioned into sub-clusters, each with `complexity` + `produces` attrs.
4. Pre-filter by `complexity` and `produces` before reading any leaf.
5. Read selected leaf `knowledge/<tier>/<group>/<slug>/AGENTS.md` (envelope) and on-demand `content/*.xml`.

The Agent SDK retriever does this automatically — see `scripts/retrieve.py`.

## Methodology layout (v3, post-F-066)

```
knowledge/<tier>/<group>/<slug>/
├── AGENTS.md                          # frontmatter (14 keys) + 11 body sections
│                                      # incl. "**Ефективно для:**" + "## Decision tree"
└── content/
    ├── 01-core-rules.xml              # ≥5 testable rules + rationale + source
    ├── 02-output-contract.xml         # JSON Schema + valid/invalid examples
    ├── 03-failure-modes.xml           # ≥3 antipatterns (symptom/root-cause/fix)
    ├── 04-procedure.xml               # step-by-step (medium/deep)
    ├── 05-examples.xml                # worked example (spec/report)
    └── 06-decision-tree.xml           # MANDATORY: <root-question> + branches → conclusion(ref=rule-id)
├── templates/                         # real working skeletons + 5-line header
└── scripts/validate-<slug>.py         # output-contract validator
```

Tier gating: free reads `free/`; solo reads `free/ + solo/`; pro reads `free/ + solo/ + pro/`; geek reads all four.

**Full routing:** [SKILL.md](SKILL.md) · **Tier manifest:** [../tier-manifest.json](../tier-manifest.json) · **Validators:** `scripts/validate-*.py`

## Workflows

End-to-end orchestration patterns under [workflows/](workflows/AGENTS.md). The umbrella skill `/faion` auto-routes to one of these by context:

- `workflows/brainstorm/` — multi-agent diverge-converge-review (consent gate runs first if user did not request brainstorm)
- `workflows/sdd-batch-orchestrator/` — single-feature or multi-feature SDD batch (study → clarify → plan → wave-execute → verify → review → fix → close)
- `workflows/improver/` — session review + system audit + fix-apply-log-commit cycle
- `workflows/media-ops/` — AI media pipeline (interview → propose → scaffold → infra → content → register)
- `workflows/poll-agents/` — self-replenishing background-agent pool for long task queues

## Playbooks (parallel structure)

`playbooks/` mirrors knowledge but organised by **goal-character** (11 categories, see `playbooks/taxonomy.xml`):

`discover-validate · plan-design · build-ship · operate-ritual · govern-decide · fix-incident · optimize-tune · migrate-rebuild · acquire-grow · hire-onboard · audit-comply`

Per-playbook layout same v3 shape: `AGENTS.md` + `content/01-playbook.xml`. Tier gating same as knowledge.

L1: `playbooks/taxonomy.xml` (categories + decision-tree).
L2: `playbooks/by-goal/<goal>/INDEX.xml`.

Spec: `.aidocs/conventions/playbooks/playbook-spec.md`. Validator: `scripts/validate-playbook-v3.py`.

---

*Faion Network v5.0 — 2-level retrieval, 20 canonical domains, 11 goal categories.*
