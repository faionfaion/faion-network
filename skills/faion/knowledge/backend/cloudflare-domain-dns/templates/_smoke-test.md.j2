<!-- purpose: Minimum viable filled-in DNS plan. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Cloudflare DNS Plan — example.com

## Zone

- domain: example.com
- origin_ipv4: 203.0.113.10
- origin_ipv6: 2001:db8::10
- canonical: apex
- ssl_mode: full_strict

## Records

| type | name | content | proxied | rationale |
|------|------|---------|---------|-----------|
| A | @ | 203.0.113.10 | ON | HTTPS origin behind proxy |
| AAAA | @ | 2001:db8::10 | ON | dual-stack origin |
| CNAME | www | example.com | ON | mirror canonical |
| MX | @ | 10 mx1.mailprovider.example | n/a | mail delivered off-origin; MX never exposes the web origin |
| TXT | @ | v=spf1 include:mailprovider.example -all | n/a | SPF scoped to the mail provider only |

No `mail` A record exists in this zone: publishing one would put the origin address in
public DNS and let an attacker bypass the proxy for every hostname. See
`content/03-failure-modes.xml` → `mail-a-record-origin-leak`.

## Verify

- `dig NS example.com +short @1.1.1.1` → ns1/ns2.cloudflare.com
- `curl -I https://example.com` → HTTP/2 200, server: cloudflare
- `dig A mail.example.com +short` → NXDOMAIN (no origin address published)

**Owner:** @handle (founder)  •  **Reviewed:** 2026-05-23
