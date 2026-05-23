<!-- purpose: Minimum viable filled-in DNS plan. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Cloudflare DNS Plan — faion.net

## Zone

- domain: faion.net
- origin_ipv4: 46.225.58.119
- origin_ipv6: 2a01:4f8:c012:abcd::1
- canonical: apex
- ssl_mode: full_strict

## Records

| type | name | content | proxied | rationale |
|------|------|---------|---------|-----------|
| A | @ | 46.225.58.119 | ON | HTTPS origin behind proxy |
| AAAA | @ | 2a01:4f8:c012:abcd::1 | ON | dual-stack origin |
| CNAME | www | faion.net | ON | mirror canonical |
| A | mail | 46.225.58.119 | OFF | SMTP must hit origin |

## Verify

- `dig NS faion.net +short @1.1.1.1` → ns1/ns2.cloudflare.com
- `curl -I https://faion.net` → HTTP/2 200, server: cloudflare

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
