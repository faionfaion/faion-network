# TASK_000: Project Setup (Go)

<!-- SUMMARY: Initialize {project_name} Go project with full development infrastructure -->

## Complexity: normal
## Created: {YYYY-MM-DD}
## Project: {project_name}
## Depends on: none

---

## Description

Bootstrap Go project with:
- Go modules
- golangci-lint
- Standard project layout
- Built-in testing
- Pre-commit hooks
- GitHub Actions CI

---

## Context

- **Constitution:** `aidocs/sdd/{project_name}/constitution.md`
- **Go Version:** 1.22+
- **Module Path:** github.com/{username}/{project_name}
- **Target Directory:** `{project_path}/`

---

## Goals

1. Initialize Go module
2. Create standard project layout
3. Configure golangci-lint
4. Set up testing structure
5. Set up pre-commit hooks
6. Create GitHub Actions workflow
7. Create Makefile
8. Create README with getting started

---

## Acceptance Criteria

- [ ] `go build ./...` succeeds
- [ ] `make lint` passes
- [ ] `make test` runs
- [ ] `make fmt` formats code
- [ ] Git hooks work
- [ ] CI pipeline is green
- [ ] README has getting started

---

## Technical Notes

```
cmd/{app}/main.go - Entry points
internal/ - Private packages
pkg/ - Public packages
.golangci.yml - Linter config
Makefile - Developer commands
```

---

## Out of Scope

- Application logic
- Database setup
- API implementation
- Deployment config

---

## Subtasks

- [ ] 01. Create project directory
- [ ] 02. Initialize Go module:
  ```bash
  go mod init github.com/{username}/{project_name}
  ```
- [ ] 03. Create directory structure:
  ```
  {project_name}/
  ├── cmd/{app}/
  │   └── main.go
  ├── internal/
  │   └── .gitkeep
  ├── pkg/
  │   └── .gitkeep
  ├── tests/
  │   └── .gitkeep
  └── docs/
  ```
- [ ] 04. Create initial main.go:
  ```go
  package main

  func main() {
      println("Hello, {project_name}!")
  }
  ```
- [ ] 05. Configure golangci-lint (.golangci.yml):
  ```yaml
  run:
    timeout: 5m

  linters:
    enable:
      - errcheck
      - gosimple
      - govet
      - ineffassign
      - staticcheck
      - unused
      - gofmt
      - goimports
      - misspell
      - unconvert
      - unparam
      - revive

  linters-settings:
    gofmt:
      simplify: true
    revive:
      rules:
        - name: blank-imports
        - name: context-as-argument
        - name: error-return
        - name: error-strings
        - name: exported
  ```
- [ ] 06. Create Makefile:
  ```makefile
  .PHONY: build run test lint fmt clean all

  BINARY_NAME={project_name}

  build:
  	go build -o bin/$(BINARY_NAME) ./cmd/{app}

  run:
  	go run ./cmd/{app}

  test:
  	go test -v -race -cover ./...

  lint:
  	golangci-lint run

  fmt:
  	gofmt -s -w .
  	goimports -w .

  clean:
  	rm -rf bin/

  all: fmt lint test build
  ```
- [ ] 07. Create .pre-commit-config.yaml:
  ```yaml
  repos:
    - repo: https://github.com/golangci/golangci-lint
      rev: v1.62.0
      hooks:
        - id: golangci-lint
    - repo: https://github.com/pre-commit/pre-commit-hooks
      rev: v4.6.0
      hooks:
        - id: trailing-whitespace
        - id: end-of-file-fixer
  ```
- [ ] 08. Create .gitignore:
  ```
  # Binaries
  bin/
  *.exe
  *.dll
  *.so
  *.dylib

  # Test
  *.test
  *.out
  coverage.txt

  # IDE
  .idea/
  .vscode/
  *.swp

  # OS
  .DS_Store
  ```
- [ ] 09. Create .github/workflows/ci.yml:
  ```yaml
  name: CI
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-go@v5
          with:
            go-version: '1.22'
        - name: golangci-lint
          uses: golangci/golangci-lint-action@v6
        - run: go test -v -race -cover ./...
        - run: go build ./...
  ```
- [ ] 10. Initialize pre-commit:
  ```bash
  pre-commit install
  ```
- [ ] 11. Create README.md:
  ```markdown
  # {project_name}

  ## Getting Started

  ### Prerequisites
  - Go 1.22+
  - golangci-lint
  - pre-commit (optional)

  ### Installation
  ```bash
  git clone https://github.com/{username}/{project_name}
  cd {project_name}
  pre-commit install  # optional
  ```

  ### Development
  ```bash
  make run      # Run the application
  make test     # Run tests
  make lint     # Run linter
  make build    # Build binary
  make all      # Format, lint, test, build
  ```
  ```
- [ ] 12. Initial commit

---

## Implementation

<!-- To be filled by executor -->

---

## Summary

<!-- To be filled after completion -->
