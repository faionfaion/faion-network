# M-RB-004: Ruby Code Quality

## Metadata
- **Category:** Development/Backend/Ruby
- **Difficulty:** Beginner
- **Tags:** #dev, #ruby, #quality, #rubocop, #methodology
- **Agent:** faion-code-agent

---

## Problem

Ruby's flexibility enables many coding styles. Without standards, codebases become inconsistent. Code reviews waste time on style instead of logic. Security issues slip through.

## Promise

After this methodology, your Ruby code will be consistent, secure, and maintainable. Automated tools will catch issues before review.

## Overview

Ruby code quality uses RuboCop for style, Brakeman for security, and various tools for documentation. This methodology covers the complete quality stack.

---

## Framework

### Step 1: RuboCop Configuration

**Gemfile:**

```ruby
group :development, :test do
  gem 'rubocop', require: false
  gem 'rubocop-rails', require: false
  gem 'rubocop-rspec', require: false
  gem 'rubocop-performance', require: false
end
```

**.rubocop.yml:**

```yaml
require:
  - rubocop-rails
  - rubocop-rspec
  - rubocop-performance

AllCops:
  NewCops: enable
  TargetRubyVersion: 3.3
  SuggestExtensions: false
  Exclude:
    - 'db/schema.rb'
    - 'db/migrate/**/*'
    - 'vendor/**/*'
    - 'bin/**/*'
    - 'node_modules/**/*'
    - 'tmp/**/*'

# Style
Style/Documentation:
  Enabled: false

Style/FrozenStringLiteralComment:
  Enabled: true
  EnforcedStyle: always

Style/StringLiterals:
  EnforcedStyle: single_quotes

Style/HashSyntax:
  EnforcedStyle: ruby19_no_mixed_keys

Style/TrailingCommaInHashLiteral:
  EnforcedStyleForMultiline: comma

Style/TrailingCommaInArrayLiteral:
  EnforcedStyleForMultiline: comma

# Layout
Layout/LineLength:
  Max: 120
  AllowedPatterns: ['^\s*#']

Layout/MultilineMethodCallIndentation:
  EnforcedStyle: indented

Layout/FirstHashElementIndentation:
  EnforcedStyle: consistent

# Metrics
Metrics/MethodLength:
  Max: 20
  CountAsOne: ['array', 'heredoc', 'hash']

Metrics/ClassLength:
  Max: 200
  CountAsOne: ['array', 'heredoc', 'hash']

Metrics/BlockLength:
  Exclude:
    - 'spec/**/*'
    - 'config/routes.rb'
    - '*.gemspec'

Metrics/AbcSize:
  Max: 25

# Rails
Rails/I18nLocaleTexts:
  Enabled: false

Rails/SkipsModelValidations:
  Exclude:
    - 'spec/**/*'

# RSpec
RSpec/ExampleLength:
  Max: 15

RSpec/MultipleExpectations:
  Max: 5

RSpec/NestedGroups:
  Max: 4

RSpec/DescribeClass:
  Exclude:
    - 'spec/requests/**/*'
    - 'spec/system/**/*'

# Performance
Performance/Casecmp:
  Enabled: true
```

### Step 2: Security with Brakeman

```bash
# Add to Gemfile
gem 'brakeman', require: false

# Run scan
bundle exec brakeman

# With specific output
bundle exec brakeman -o brakeman-output.html -o brakeman-output.json
```

**brakeman.ignore:**

```yaml
# Ignore specific warnings
ignore:
  - fingerprint: "abc123..."
    reason: "False positive - input is sanitized"
```

### Step 3: Dependency Auditing

```bash
# Add to Gemfile
gem 'bundler-audit', require: false

# Run audit
bundle audit check --update

# In CI
bundle audit check
```

### Step 4: Code Complexity

**Gemfile:**

```ruby
gem 'reek', require: false
gem 'flay', require: false
```

**Reek (code smells):**

```bash
# Run reek
bundle exec reek app lib

# With config
bundle exec reek -c .reek.yml
```

**.reek.yml:**

```yaml
detectors:
  TooManyStatements:
    max_statements: 10
    exclude:
      - 'initialize'

  UncommunicativeVariableName:
    accept:
      - 'e'  # exception
      - 'i'  # iterator
      - 'n'  # number

  UtilityFunction:
    enabled: false

  IrresponsibleModule:
    enabled: false
```

**Flay (duplication):**

```bash
bundle exec flay app lib
```

### Step 5: Documentation

**YARD Setup:**

```ruby
gem 'yard', require: false
```

```ruby
# @param name [String] the user's name
# @param age [Integer] the user's age
# @return [User] the created user
# @raise [ValidationError] if validation fails
def create_user(name:, age:)
  # ...
end
```

```bash
# Generate docs
bundle exec yard doc

# Start server
bundle exec yard server
```

### Step 6: Automation

**Makefile:**

```makefile
.PHONY: lint security test quality

lint:
	bundle exec rubocop

lint-fix:
	bundle exec rubocop -a

security:
	bundle exec brakeman -q
	bundle exec bundle audit check

test:
	bundle exec rspec

quality: lint security test
	@echo "All quality checks passed!"
```

**Pre-commit hook (.git/hooks/pre-commit):**

```bash
#!/bin/sh

# Run RuboCop on staged files
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.rb$')

if [ -n "$FILES" ]; then
  bundle exec rubocop $FILES
  if [ $? -ne 0 ]; then
    echo "RuboCop failed. Fix issues before committing."
    exit 1
  fi
fi

exit 0
```

---

## Templates

### CI Configuration

**.github/workflows/quality.yml:**

```yaml
name: Quality

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
          bundler-cache: true

      - name: RuboCop
        run: bundle exec rubocop --format github

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
          bundler-cache: true

      - name: Brakeman
        run: bundle exec brakeman -q --no-exit-on-warn

      - name: Bundle Audit
        run: bundle exec bundle audit check --update

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
          bundler-cache: true

      - name: Setup DB
        run: bundle exec rails db:setup
        env:
          RAILS_ENV: test
          DATABASE_URL: postgres://postgres:postgres@localhost/test

      - name: RSpec
        run: bundle exec rspec
        env:
          RAILS_ENV: test
          DATABASE_URL: postgres://postgres:postgres@localhost/test
```

### VS Code Settings

**.vscode/settings.json:**

```json
{
  "editor.formatOnSave": true,
  "[ruby]": {
    "editor.defaultFormatter": "rubocop"
  },
  "ruby.rubocop.executePath": "bundle exec rubocop"
}
```

---

## Examples

### Custom RuboCop Cop

```ruby
# lib/rubocop/cop/custom/no_puts.rb
module RuboCop
  module Cop
    module Custom
      class NoPuts < Base
        MSG = 'Avoid using puts, use Rails.logger instead.'

        def on_send(node)
          return unless node.method_name == :puts

          add_offense(node)
        end
      end
    end
  end
end
```

### Rubocop TODO for Legacy Code

```bash
# Generate TODO file for legacy code
bundle exec rubocop --auto-gen-config

# This creates .rubocop_todo.yml
# Include in main config
```

```yaml
# .rubocop.yml
inherit_from: .rubocop_todo.yml
```

---

## Common Mistakes

1. **Disabling all cops** - Fix issues, don't ignore them
2. **Ignoring security warnings** - Address Brakeman issues
3. **No CI enforcement** - Checks must run on every PR
4. **Not updating cops** - Keep RuboCop current
5. **Inconsistent config** - Share config across projects

---

## Checklist

- [ ] RuboCop configured with Rails/RSpec extensions
- [ ] Brakeman for security scanning
- [ ] Bundle audit for dependency vulnerabilities
- [ ] Reek for code smells (optional)
- [ ] CI runs all quality checks
- [ ] Pre-commit hooks for local checks
- [ ] VS Code/editor integration
- [ ] Team aligned on rules

---

## Next Steps

- M-RB-001: Ruby Project Setup
- M-RB-003: Ruby Testing with RSpec
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-RB-004 v1.0*
