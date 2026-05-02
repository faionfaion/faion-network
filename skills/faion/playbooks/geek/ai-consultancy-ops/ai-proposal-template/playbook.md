---
name: ai-proposal-template
description: Write a winning AI engagement proposal covering problem, architecture, scope, ROI, risk, timeline, and pricing for a client MVP.
tier: geek
group: ai-consultancy-ops
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a complete AI engagement proposal document that a client can sign off on — covering problem statement, proposed AI solution with architecture sketch, scope (in/out), quantified ROI, a risk register with mitigations, a 4–6-week timeline, and a pricing breakdown from $30k–$80k for an MVP.

## Prerequisites

- A defined client engagement (discovery call completed, business problem understood).
- Access to the client's approximate user count, support ticket volume (or equivalent operational metric), and average hourly labour cost.
- Familiarity with Anthropic Claude API (`anthropic>=0.40`) and at least one integration pattern (agent loop, RAG pipeline, or classifier).
- Optional: read the `multi-agent-basics` methodology for multi-agent architecture choices.

## Steps

1. **Write the Problem Statement section.**
   State the client's pain in one paragraph using their own words from discovery. Include the measurable symptom (e.g., "1 200 support tickets/month resolved manually at avg 8 min per ticket, $24 FTE-cost per resolution"). Avoid diagnosis at this stage — that comes in the next section.

2. **Sketch the Proposed AI Solution.**
   Choose one of three architecture patterns based on the use case:

   | Pattern | When to choose | Stack |
   |---------|----------------|-------|
   | Single-agent classifier | Classification / routing, <500 ms SLA | `claude-haiku-4-5-20251001`, Pydantic v2 schema output |
   | RAG-augmented responder | Knowledge-intensive Q&A or drafting | `claude-sonnet-4-6` + pgvector (Postgres 16) |
   | Multi-agent pipeline | Complex workflows with branching decisions | `claude-opus-4-7` orchestrator + `claude-sonnet-4-6` workers |

   Example architecture sketch for "AI customer support agent for SaaS at $50k":

   ```
   Inbound ticket (webhook)
     → Classifier (claude-haiku-4-5-20251001, Pydantic schema)
         → intent: billing / technical / general
     → RAG responder (claude-sonnet-4-6 + pgvector knowledge base)
         → draft reply with citations
     → Human-in-the-loop gate (confidence < 0.85 → escalate)
     → Zendesk API → post reply
   ```

   Python skeleton (Anthropic SDK 2026):

   ```python
   import anthropic
   from pydantic import BaseModel

   class TicketIntent(BaseModel):
       intent: str        # "billing" | "technical" | "general"
       confidence: float  # 0.0–1.0
       summary: str       # ≤40-word summary for downstream prompt

   client = anthropic.Anthropic()

   def classify_ticket(ticket_body: str) -> TicketIntent:
       response = client.messages.create(
           model="claude-haiku-4-5-20251001",
           max_tokens=256,
           messages=[{"role": "user", "content": ticket_body}],
           system=(
               "Classify the support ticket. "
               "Return JSON matching: "
               '{"intent":"billing|technical|general","confidence":0.0-1.0,"summary":"..."}'
           ),
       )
       return TicketIntent.model_validate_json(response.content[0].text)
   ```

3. **Define Scope (in/out).**

   | In scope | Out of scope |
   |----------|--------------|
   | Ticket intake via Zendesk webhook | CRM integration with Salesforce |
   | Intent classification + RAG-drafted replies | Proactive outreach / marketing emails |
   | Human escalation gate (confidence threshold) | Model fine-tuning or custom model training |
   | Deployment on client AWS account (ECS Fargate) | Ongoing model retraining pipeline |
   | 60-day post-launch hypercare | SLA monitoring tooling (client responsibility) |

4. **Calculate ROI.**
   Use this formula:

   ```
   Monthly saving = (tickets/month × avg_handle_min / 60) × hourly_cost × automation_rate
   Annual saving   = monthly_saving × 12
   Payback period  = project_cost / monthly_saving
   ```

   Worked example ($50k AI customer support agent):
   - 1 200 tickets/month × 8 min avg handle = 160 h/month
   - 160 h × $30/h FTE cost = $4 800/month saved at 100% automation
   - Realistic 70% automation rate → $3 360/month
   - Annual saving: $40 320
   - Project cost: $50 000 → payback 14.9 months
   - Year 2 ROI: $40 320 / $50 000 = 81%

   Include a 3-column table in the proposal (Conservative / Base / Optimistic) varying automation rate from 55% to 80%.

5. **Build the Risk Register.**

   | Risk | Likelihood | Impact | Mitigation |
   |------|-----------|--------|------------|
   | Model accuracy below threshold (<85% intent accuracy) | Medium | High | Pilot on 200 historical tickets before go-live; add human-review queue |
   | Hallucinated reply sent to customer | Low | High | Confidence gate (threshold 0.85); RAG citations returned with every draft; human approval for first 2 weeks |
   | Cost overrun (API spend >budget) | Medium | Medium | Set Anthropic usage limits; use `claude-haiku-4-5-20251001` for classification (≈$0.0008/1k tokens); daily spend alert |
   | Data privacy / PII leak | Low | Critical | Strip PII before sending to Claude API (regex + Presidio); data processing agreement (DPA) with Anthropic |
   | Scope creep extending timeline | High | Medium | Fixed-scope contract clause; change-request process documented in proposal |

6. **Lay out the Timeline (4–6 weeks).**

   | Week | Milestone | Deliverable |
   |------|-----------|-------------|
   | 1 | Discovery & data audit | Dataset of 500+ historical tickets labelled; integration spec |
   | 2 | Core pipeline build | Classifier + RAG pipeline running locally against test dataset |
   | 3 | Integration & staging | Zendesk webhook wired; confidence gate configured; staging env on AWS |
   | 4 | UAT & tuning | Client acceptance testing; accuracy ≥85% on held-out 100 tickets |
   | 5 | Hardening & docs | Load test (50 concurrent tickets); runbook; DPA signed |
   | 6 (optional) | Go-live & hypercare | Production launch; daily check-ins for 14 days |

7. **Present Pricing.**

   Use a three-tier table:

   | Package | Scope | Price |
   |---------|-------|-------|
   | Starter (4 weeks) | Classifier + static-response lookup, no RAG | $30 000 |
   | Standard (5 weeks) | Classifier + RAG-drafted replies + human gate | $50 000 |
   | Advanced (6 weeks) | Standard + multi-agent escalation + Slack ops dashboard | $80 000 |

   Payment terms: 40% on signing, 40% on staging sign-off, 20% on go-live.
   Monthly retainer (post-launch support): $2 500/month, 3-month minimum.

8. **Add Success Metrics.**
   Include a table that maps each goal to a KPI and a measurement method:

   | Success metric | Target | Measurement |
   |----------------|--------|-------------|
   | Ticket automation rate | ≥70% fully auto-resolved | Zendesk custom field `ai_resolved` |
   | First-response time | <2 min (was 4 h) | Zendesk report: avg first-response |
   | Customer CSAT on AI-handled tickets | ≥4.0 / 5.0 | Post-resolution survey |
   | API cost per ticket | <$0.04 | Anthropic usage dashboard |
   | Human escalation rate | <30% of intake | Zendesk escalation tag count |

## Verify

Open the draft proposal document and run this checklist:

```
grep -c "## " proposal-draft.md   # should return exactly 8 (8 sections)
```

Confirm each required section heading is present:

```
Problem Statement | Proposed AI Solution | Scope | ROI | Risk Register | Timeline | Pricing | Success Metrics
```

Then send a one-page executive summary to a non-technical stakeholder for feedback. If they can explain back what the AI will do and what it costs, the proposal is clear enough to send.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Client asks "what model do you use?" without reading section 2 | Architecture section too technical | Add a one-sentence plain-English description above the architecture diagram: "We use Anthropic's Claude AI, the same technology behind Claude.ai, hosted on your AWS account." |
| Client pushes back on price ("seems expensive") | ROI section not compelling | Anchor to annual saving first, then present price as fraction of Year 1 saving. If payback > 18 months, reduce scope to Starter package. |
| Scope creep request during proposal review | Unclear in/out scope table | Reference the scope table explicitly: "That's out of scope for this engagement — we can quote it as a Phase 2." |
| Client wants a longer timeline than 6 weeks | Risk aversion or internal politics | Offer an optional Week 7 "shadowing period" where AI runs in read-only mode alongside human agents — no extra cost, just timeline extension. |
| ROI calc rejected ("our cost per ticket is lower") | Wrong input assumptions | Ask client for exact labour cost data; recalculate live in the call using the formula in Step 4. |

## Next

- Run a scoping workshop with the client using the `pro/marketing/gtm-strategist/growth-gtm-strategy` methodology to align on business goals before drafting.
- After signing, run the `geek/ai-agents/multi-agent-basics` methodology sprint to validate the chosen architecture against the actual data.
- Price the retainer using `pro/marketing/gtm-strategist/ops-financial-basics` unit-economics model to ensure monthly recurring margin ≥40%.

## References

- [knowledge/pro/marketing/gtm-strategist/growth-gtm-strategy](../../../knowledge/pro/marketing/gtm-strategist/growth-gtm-strategy) — GTM strategy framing drives the problem statement and success metrics sections; the methodology's market-sizing templates back the ROI conservative/base/optimistic columns.
- [knowledge/pro/marketing/gtm-strategist/ops-financial-basics](../../../knowledge/pro/marketing/gtm-strategist/ops-financial-basics) — unit-economics and pricing-tier models underpin the three-package pricing table and the monthly retainer margin calculation.
- [knowledge/geek/ai/ai-agents/multi-agent-basics](../../../knowledge/geek/ai/ai-agents/multi-agent-basics) — multi-agent architecture patterns (orchestrator + workers) inform the Advanced package scope and the architecture sketch in Step 2.
- [knowledge/geek/ai/ai-agents/ai-governance-compliance](../../../knowledge/geek/ai/ai-agents/ai-governance-compliance) — AI governance and compliance requirements directly populate the data-privacy and PII risk rows in the Risk Register.
