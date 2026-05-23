<!-- purpose: Markdown skeleton for the Azure architecture spec -->
<!-- consumes: inputs declared in AGENTS.md `## Prerequisites` -->
<!-- produces: artefact conforming to content/02-output-contract.xml (spec) -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~400 tokens when loaded -->

# Azure Architecture Spec

- **Org:** 
- **Tenant:** 
- **Author:** 
- **Date:** 

## Management group hierarchy

```
root
├── platform
│   ├── identity
│   ├── management
│   └── connectivity
└── landingzones
    ├── corp
    └── online
```

## Policy initiative

- Name: 
- Required policies: deny-public-IP, require-encryption, allowed-locations

## Identity

- Entra ID tenant: 
- Managed Identity scope: 
- PIM groups: 

## Network

- Topology: hub-spoke / VWAN
- Private Endpoints: 
- DNS: Azure Private DNS zones

## BCDR

- Azure Backup immutable vault: 
- Site Recovery RTO/RPO: 
