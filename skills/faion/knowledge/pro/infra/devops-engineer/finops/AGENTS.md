# FinOps

## Summary

Cloud Financial Operations: the Inform → Optimize → Operate cycle for cloud cost management. Organizations waste 32% of cloud spend (~$200B/year globally). FinOps teams achieve 10-20x ROI within 30-60 days by making cost visible (tagging), eliminating waste (rightsizing, idle resources), and committing (Savings Plans/Reserved Instances).

## Why

Cloud bills grow unchecked without ownership. FinOps assigns cost accountability to engineering teams via mandatory tags (Environment, Owner, Project, CostCenter), automated anomaly detection, and per-team budget alerts. AI/ML workloads are a special case: GPU costs are 5-10x standard compute, requiring checkpointing + spot instances for training and batching/caching for inference.

## When To Use

- Cloud monthly spend exceeds $10k and cost attribution is unclear
- Engineering teams have no visibility into their own cloud costs
- Preparing Savings Plan or Reserved Instance purchases (need 30+ days baseline)
- Rightsizing instances where avg CPU is below 20% or memory below 30%
- AI/ML training workloads where GPU instances run on-demand without checkpointing

## When NOT To Use

- Pre-production environments with no steady-state usage patterns — optimization signal is noisy
- When cost data is less than 30 days old — too early for commitment recommendations
- As a substitute for architecture decisions (e.g., using FinOps to offset a fundamentally overprovisioned design)

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Three phases (Inform/Optimize/Operate), savings percentages per strategy, AI/ML cost patterns |
| `content/02-checklist.xml` | Tagging rules, anomaly detection setup, rightsizing analysis, commitment discount steps |
| `content/03-examples.xml` | Idle instance detection script, savings plan calculation, S3 lifecycle optimization, SCP for budget governance |

## Templates

| File | Purpose |
|------|---------|
| `templates/tagging-policy.yaml` | Mandatory tag schema: Environment, Owner, Project, CostCenter with allowed values |
| `templates/budget.tf` | Terraform AWS budget with 50/80/100/120% alerts and forecasted overage alert |
| `templates/cost-report.md` | Monthly cloud cost report template with team breakdown and optimization table |
| `templates/prompt-cost-analysis.txt` | LLM prompt for cost breakdown and rightsizing recommendations |
