---
id: security-as-code
name: "Security as Code (DevSecOps)"
domain: OPS
skill: faion-cicd-engineer
category: "best-practices-2026"
---

# Security as Code (DevSecOps)

## Overview

Security as Code (SaC) integrates security checks, threat modeling, testing, and vulnerability scanning directly into the CI/CD pipeline. It provides real-time security feedback and enables early vulnerability detection through automated, codified security policies.

## Problem

- Manual security policies don't scale in dynamic environments
- Compliance gaps in cloud-native architectures
- Late-stage vulnerability detection increases remediation costs
- Security bottlenecks slow down development velocity

## Solution

Implement security controls as code throughout the SDLC:

1. **SAST** - Static Application Security Testing (source code analysis)
2. **DAST** - Dynamic Application Security Testing (runtime analysis)
3. **Container Scanning** - Image vulnerability detection
4. **Policy as Code** - Automated compliance enforcement

## Key Components

### 1. Static Application Security Testing (SAST)

Analyzes source code before execution to identify vulnerabilities early.

| Tool | Approach | Accuracy | Best For |
|------|----------|----------|----------|
| CodeQL | Semantic analysis | 88% / 5% FP | GitHub-centric teams |
| Snyk Code | AI-driven | 85% / 8% FP | Open-source heavy projects |
| Semgrep | Pattern matching | 82% / 12% FP | Custom rule flexibility |
| SonarQube | Quality + security | Good | Code quality focus |

**Key Insight:** SAST catches vulnerabilities before deployment but may miss runtime issues. Best for "shift-left" security.

### 2. Dynamic Application Security Testing (DAST)

Tests running applications to find vulnerabilities in production-like environments.

| Tool | Type | Cost | Best For |
|------|------|------|----------|
| OWASP ZAP | Open-source | Free | Startups, small teams |
| Burp Suite | Commercial | $$$ | Penetration testing |
| Nuclei | Template-based | Free | CI/CD automation |

**Key Insight:** DAST finds runtime vulnerabilities but requires running application. Best for "shift-right" security.

### 3. Container Security Scanning

Scans container images for known vulnerabilities before deployment.

| Tool | Maintainer | Approach | Best For |
|------|------------|----------|----------|
| Trivy | Aqua Security | All-in-one | CI/CD pipelines |
| Grype | Anchore | Focused | SBOM generation |
| Clair | Red Hat | Layer-by-layer | Registry integration |

**Key Insight:** 87% of production container images have at least one major vulnerability (2024 Cloud Native Security Report).

### 4. Policy as Code

Codifies and automates compliance and security policies.

| Tool | Language | Scope | Learning Curve |
|------|----------|-------|----------------|
| OPA | Rego | Multi-system | Steeper |
| Gatekeeper | Rego + CRDs | Kubernetes | Moderate |
| Kyverno | YAML | Kubernetes | Easier |

**Key Insight:** 96% of technical decision-makers say Policy as Code is vital for secure, scalable cloud operations.

## DevSecOps Trends 2026

1. **Shift-Smart Security** - Context-aware security in the IDE
2. **AI as DevSecOps Teammate** - From detection to prediction
3. **Supply Chain Hardening** - Critical infrastructure protection
4. **Policy as Code Adoption** - Zero Trust enforcement
5. **SBOM Requirements** - Software Bill of Materials mandates

## Integration Strategy

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Commit    │ --> │    Build    │ --> │   Deploy    │ --> │   Runtime   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │                   │
      v                   v                   v                   v
   ┌──────┐          ┌──────────┐        ┌──────────┐        ┌──────┐
   │ SAST │          │ Container│        │ Policy   │        │ DAST │
   │ SCA  │          │ Scanning │        │ as Code  │        │ RASP │
   │Secret│          │ SBOM     │        │ Admission│        │ WAF  │
   └──────┘          └──────────┘        └──────────┘        └──────┘
```

## Quick Start

1. **Start with SAST** - Integrate Semgrep or CodeQL in CI
2. **Add Container Scanning** - Use Trivy for image scans
3. **Implement Policy as Code** - Start with Kyverno for simplicity
4. **Add DAST** - Use ZAP or Nuclei for runtime testing
5. **Enable SBOM** - Generate with Syft or Trivy

## Folder Contents

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Code examples for each tool |
| [templates.md](templates.md) | Ready-to-use templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for security tasks |

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Set up GitHub Actions workflow from template | haiku | Pattern application, simple configuration |
| Design CI/CD pipeline architecture | opus | Complex system design with many variables |
| Write terraform code for infrastructure | sonnet | Implementation with moderate complexity |
| Debug failing pipeline step | sonnet | Debugging and problem-solving |
| Implement AIOps anomaly detection | opus | Novel ML approach, complex decision |
| Configure webhook and secret management | haiku | Mechanical setup using checklists |


## Sources

- [DevSecOps Best Practices 2026](https://www.practical-devsecops.com/devsecops-best-practices/)
- [DevSecOps Trends 2026](https://www.practical-devsecops.com/devsecops-trends-2026/)
- [Security as Code Building Blocks](https://www.jit.io/resources/devsecops/security-as-code-building-blocks)
- [Open Policy Agent Documentation](https://www.openpolicyagent.org/docs/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [SAST vs DAST](https://www.wiz.io/academy/application-security/sast-vs-dast)
- [Container Scanning Tools 2026](https://www.aikido.dev/blog/top-container-scanning-tools)
