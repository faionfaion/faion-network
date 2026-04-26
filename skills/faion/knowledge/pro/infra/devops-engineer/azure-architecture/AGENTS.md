# Azure Architecture

## Summary

Azure enterprise architecture is organized around the Well-Architected Framework (five pillars: Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency) and Landing Zones (eight design areas). Use Azure Verified Modules (AVM) and Bicep for new deployments; the legacy ESLZ Terraform module is deprecated as of August 2026.

## Why

Landing Zones establish governance guardrails before workloads arrive — management group hierarchy, Azure Policy, RBAC, and networking — preventing retrofitting compliance onto running systems. Policy-driven governance via Azure Policy Initiative enforces standards automatically across all subscriptions without per-team enforcement overhead.

## When To Use

- Designing new Azure workload from scratch and need governance baseline
- Organization is adopting Azure at scale (multiple subscriptions, multiple teams)
- Evaluating Well-Architected Framework pillars against an existing Azure deployment
- Setting up hub-spoke networking, Entra ID integration, or PIM-based privileged access
- Migrating on-premises workloads following Cloud Adoption Framework patterns

## When NOT To Use

- Single-subscription, single-team project without compliance requirements — Landing Zone overhead is not justified; use a simple resource group structure
- Non-Azure cloud (AWS, GCP) — framework is Azure-specific; use respective cloud frameworks
- Proof-of-concept or sandbox environment — apply minimal governance, not full Landing Zone

## Content

| File | What's inside |
|------|---------------|
| `content/01-well-architected.xml` | Five pillars with concrete implementation guidance per pillar |
| `content/02-landing-zones.xml` | Eight design areas, management group hierarchy, governance patterns, IaC tooling (AVM, Bicep) |

## Templates

| File | Purpose |
|------|---------|
| `templates/management-group-hierarchy.md` | Standard management group tree (Platform/LandingZones/Sandbox/Decommissioned) |
| `templates/prompt-design.txt` | LLM prompt for Azure architecture design review |
