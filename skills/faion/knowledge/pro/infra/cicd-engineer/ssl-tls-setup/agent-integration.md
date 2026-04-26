# Agent Integration — SSL/TLS Setup

## When to use
- Issuing and rotating certificates for public web/API endpoints (Let's Encrypt, ZeroSSL, commercial CA).
- Setting up cert-manager in Kubernetes for ingress/Gateway certs.
- Configuring TLS termination on NGINX, HAProxy, Envoy, ALB, Cloud Run, or App Gateway.
- Mutual TLS (mTLS) for service-to-service auth, internal CAs (`step-ca`, AWS Private CA, Vault PKI).
- Hardening cipher suites and protocol versions to TLS 1.3 + TLS 1.2 fallback only.
- Certificate inventory + expiry alerting.

## When NOT to use
- Internal-only dev environments where `mkcert` self-signed is sufficient and not regulated.
- Service-mesh mTLS — that's the mesh's job (Linkerd/Istio/Cilium auto-rotate identities); don't hand-roll.
- App-layer encryption (envelope encryption of payloads, JWE) — different methodology.
- Legacy systems mandated to use TLS 1.0/1.1 — you have a compliance/risk problem, not a setup problem.
- VPN/IPSec — these use different protocols and CAs.

## Where it fails / limitations
- Certificate renewal is the #1 outage cause; ACME failures from rate limits, DNS propagation, or HTTP-01 challenge path mismatches all silently expire.
- Short-lived certs (Let's Encrypt 6-day or upcoming 45-day) require automation; manual renewal will break.
- Cipher policy drift: copy-pasted cipher lists from old guides re-introduce CBC, RC4, or 3DES.
- HSTS misconfig: `preload` + wrong domain → permanent unreachable subdomain.
- mTLS at scale: revocation (CRL/OCSP) is hard; short-lived certs are the de-facto answer.
- Wildcard certs sprawl across teams; key compromise → mass rotation pain.
- Certificate Transparency log monitoring is often forgotten; rogue issuance goes undetected.

## Agentic workflow
Two distinct flows: (1) issuance/automation — agent authors cert-manager `ClusterIssuer` + `Certificate` CRDs, ACME client config, or AWS ACM/GCP Certificate Manager IaC. (2) hardening — agent renders TLS config blocks (NGINX, HAProxy, Envoy) from Mozilla SSL Configuration Generator output for the chosen profile (modern/intermediate). Always follow author → render → scan (`testssl.sh`, SSL Labs) → diff → apply via IaC. Never let an agent commit private keys to Git. Use SOPS/Vault/External Secrets for any private material.

### Recommended subagents
- `faion-sdd-executor-agent` — cert-manager / IaC implementation with quality gates.
- Custom `tls-hardener` — renders NGINX/HAProxy/Envoy TLS blocks from a profile spec.
- Custom `cert-inventory-agent` — scrapes ingress/ALB/listeners and emits CSV of `domain, issuer, expires_at, days_left, sans`.
- `password-scrubber-agent` — sanitizes any stray private keys or API tokens in agent-handled files.

### Prompt pattern
"You are a TLS hardener for NGINX 1.27. Output `ssl_*` directives for Mozilla `intermediate` profile, OCSP stapling enabled, HSTS `max-age=63072000; includeSubDomains; preload`, ALPN h2,http/1.1. Refuse if asked to enable TLS 1.0/1.1 or any cipher containing `RC4|3DES|CBC|MD5|SHA1`."

"You are a cert-manager author. Input: `{cluster_issuer: letsencrypt-prod, domains: [api.example.com, *.api.example.com], dns01: route53}`. Output `ClusterIssuer` and `Certificate` YAML, `privateKey.rotationPolicy: Always`, `duration: 2160h`, `renewBefore: 720h`."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `certbot` | Let's Encrypt ACME client | https://certbot.eff.org/ |
| `acme.sh` | Pure-shell ACME client (DNS-01 friendly) | https://github.com/acmesh-official/acme.sh |
| `lego` | Go-based ACME library/CLI | https://go-acme.github.io/lego/ |
| `step` (smallstep) | CA + cert ops, internal PKI | https://smallstep.com/docs/step-cli/ |
| `step-ca` | Self-hosted ACME/CA server | https://smallstep.com/docs/step-ca/ |
| `openssl` | CSRs, inspections, conversions | https://www.openssl.org/ |
| `cfssl` | Cloudflare PKI toolkit | https://github.com/cloudflare/cfssl |
| `mkcert` | Local-trusted dev certs | https://github.com/FiloSottile/mkcert |
| `testssl.sh` | Endpoint TLS scan | https://testssl.sh/ |
| `sslyze` | Programmatic TLS scan (Python) | https://github.com/nabla-c0d3/sslyze |
| `cert-manager` `cmctl` | cert-manager debugging | https://cert-manager.io/docs/reference/cmctl/ |
| `crl-monitor` / `ct-grep` | CT log monitoring | https://crt.sh/ + https://github.com/google/ct-monitor |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Let's Encrypt | Free CA | Yes — ACME | Default for public certs |
| ZeroSSL / Buypass | Free/commercial | Yes — ACME | Alternatives to LE |
| AWS Certificate Manager (ACM) | SaaS | Yes — API | Free certs for AWS resources |
| GCP Certificate Manager | SaaS | Yes — API | For GCP load balancers |
| Azure Key Vault Certificates | SaaS | Yes — API | Integrated with App Gateway/Front Door |
| cert-manager | OSS (K8s operator) | Yes — CRDs | De-facto K8s standard |
| HashiCorp Vault PKI | OSS / SaaS | Yes — API | Internal CA, short-lived certs |
| AWS Private CA | SaaS | Yes — API | Managed internal CA |
| Smallstep `step-ca` | OSS | Yes — ACME + admin API | Self-hosted internal CA |
| Cloudflare Origin CA / Edge Certs | SaaS | Yes — API | If fronted by Cloudflare |
| SSL Labs / Hardenize | SaaS | Read-only API | External hardening verification |

## Templates & scripts
See `templates.md` for NGINX/HAProxy TLS templates and cert-manager CRDs. Inline expiry sweep:

```bash
#!/usr/bin/env bash
# tls-expiry-sweep.sh — alert on certs expiring < 21 days across a domain list
set -euo pipefail
DOMAINS=${1:?file with one host:port per line, default port 443}
THRESH=${2:-21}
NOW=$(date +%s)
while read -r line; do
  [[ -z "$line" || "$line" == \#* ]] && continue
  host="${line%:*}"; port="${line##*:}"; [[ "$host" == "$port" ]] && port=443
  end=$(echo | openssl s_client -servername "$host" -connect "$host:$port" 2>/dev/null \
        | openssl x509 -noout -enddate 2>/dev/null | sed 's/notAfter=//')
  [[ -z "$end" ]] && { echo "ERR  $host:$port unreachable"; continue; }
  end_ts=$(date -d "$end" +%s)
  days=$(( (end_ts - NOW) / 86400 ))
  if (( days < THRESH )); then
    echo "WARN $host:$port expires in $days days ($end)"
  else
    echo "OK   $host:$port $days days"
  fi
done < "$DOMAINS"
```

## Best practices
- TLS 1.3 mandatory; TLS 1.2 only as fallback for legacy clients; everything older disabled.
- Mozilla `intermediate` profile by default; `modern` (TLS 1.3-only) when you control all clients.
- OCSP stapling on, must-staple where supported.
- HSTS with `max-age` ≥ 1 year and `includeSubDomains`; only add `preload` after verifying every subdomain works under HTTPS.
- Automate renewals; alert at 21 days, page at 7 days. Treat manual cert ops as an outage waiting to happen.
- Short-lived certs preferred (LE 6-day or 45-day, internal Vault 24h–7d) — reduce blast radius of key compromise.
- Separate keys per environment; never share prod keys with dev.
- Monitor Certificate Transparency for unexpected issuance against your domains.
- For mTLS: rely on a service mesh or short-lived per-pod certs, not long-lived shared client certs.
- Run `testssl.sh --severity HIGH` and SSL Labs A+ as CI gates on staging.

## AI-agent gotchas
- Cipher list copy-paste: outdated lists with `DHE-RSA-AES256-SHA` etc. — require modern Mozilla output and reject anything else.
- HTTP-01 vs DNS-01 confusion: agents pick HTTP-01 then need wildcards; flag wildcard requests and force DNS-01.
- LE rate limits: 50 certs/week per registered domain — agents iterating on issuance burn the quota; use staging endpoint first.
- Wrong key algorithm: defaulting to RSA-2048 when ECDSA P-256 is faster and standard now.
- Path mismatches in cert-manager: `Issuer` vs `ClusterIssuer`, `secretName` vs Ingress TLS `secretName` typos go silent.
- Private key leakage: agents paste keys into chat for "debugging"; enforce a no-key-in-context rule.
- Auto-renewal silent failure: cert renewed but reverse-proxy not reloaded — require post-renew hook validation.
- HSTS preload self-DoS: agents enable `preload` then can't host a subdomain over HTTPS — preload only after audit.

## References
- Mozilla SSL Configuration Generator: https://ssl-config.mozilla.org/
- Let's Encrypt docs: https://letsencrypt.org/docs/
- LE 6-day certs: https://letsencrypt.org/2025/01/16/6-day-and-ip-certs
- SSL Labs deployment best practices: https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices
- cert-manager docs: https://cert-manager.io/docs/
- testssl.sh: https://testssl.sh/
- smallstep step-ca: https://smallstep.com/docs/step-ca/
- HashiCorp Vault PKI: https://developer.hashicorp.com/vault/docs/secrets/pki
