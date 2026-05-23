<!-- purpose: Markdown DNS plan with per-record proxy justification. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Cloudflare DNS Plan — {zone}

## Zone

- domain:
- origin_ipv4:
- origin_ipv6: (or none)
- canonical: apex | www
- ssl_mode: full_strict

## Records

| type | name | content | proxied | rationale |
|------|------|---------|---------|-----------|
| A | @ | {ipv4} | ON | HTTPS origin behind proxy |
| AAAA | @ | {ipv6} | ON | dual-stack origin |
| CNAME | www | @ | ON | mirror canonical |
| A | mail | {ipv4} | OFF | SMTP must hit origin |

## Verify

- `dig NS {zone} +short @1.1.1.1` matches assigned NS
- `dig {zone} +short @1.1.1.1` returns Cloudflare anycast IPs
- `curl -I https://{zone}` returns server: cloudflare

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
