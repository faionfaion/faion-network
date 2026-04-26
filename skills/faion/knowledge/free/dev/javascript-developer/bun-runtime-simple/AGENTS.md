# Bun Runtime

## Summary

Bun is a high-performance JavaScript runtime with built-in TypeScript support, a fast HTTP server (Bun.serve), native file I/O (Bun.file/Bun.write), built-in password hashing, automatic .env loading, and a Jest-compatible test runner. Use Hono as the preferred web framework. Bun eliminates the need for dotenv, bcrypt, node-fetch, and separate test runners.

## Why

Bun starts 8x faster than Node.js (Express) and handles 7x more requests/sec (Hono vs Express). Its built-in APIs replace common npm packages, reducing dependency surface. The unified toolchain (runtime + bundler + test runner + package manager) eliminates version mismatch issues.

## When To Use

- New TypeScript projects requiring maximum startup or throughput performance
- Projects needing a unified runtime + test + bundler toolchain
- Replacing node-fetch, bcrypt, or dotenv in an existing project
- Monorepos benefiting from Bun's fast install speed

## When NOT To Use

- AWS Lambda deployments (Bun support is limited; use Node.js target)
- Projects with C++ native addon dependencies that lack Bun bindings
- Enterprise environments with strict Node.js LTS runtime policies
- When migrating: verify all dependencies work in Bun before committing

## Content

| File | What's inside |
|------|---------------|
| `content/01-setup.xml` | Project init, bunfig.toml, native API replacements checklist |
| `content/02-server.xml` | Bun.serve native server pattern, Hono framework pattern |
| `content/03-apis.xml` | File I/O, env vars, testing, bundling patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/bunfig.toml` | Standard Bun configuration for install, test, build |
| `templates/package.json` | package.json with Bun scripts |
| `templates/tsconfig.bun.json` | tsconfig for Bun projects |
| `templates/dockerfile.bun` | Multi-stage Dockerfile for Bun production |
