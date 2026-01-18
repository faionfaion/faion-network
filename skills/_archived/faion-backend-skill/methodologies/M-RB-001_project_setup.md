# M-RB-001: Ruby Project Setup

## Metadata
- **Category:** Development/Backend/Ruby
- **Difficulty:** Beginner
- **Tags:** #dev, #ruby, #backend, #setup, #methodology
- **Agent:** faion-code-agent

---

## Problem

Ruby projects need proper gem management, version control, and environment setup. Without structure, dependency conflicts and environment mismatches cause production issues.

## Promise

After this methodology, you will have a professional Ruby project with Bundler, version management, and proper structure that works consistently across environments.

## Overview

Ruby uses Bundler for dependency management and rbenv/asdf for version management. This methodology covers setup for both Rails and non-Rails projects.

---

## Framework

### Step 1: Ruby Version Management

**Using rbenv:**

```bash
# Install rbenv
brew install rbenv ruby-build  # macOS
# or
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash

# Install Ruby version
rbenv install 3.3.0
rbenv global 3.3.0

# Create .ruby-version file
echo "3.3.0" > .ruby-version
```

**Using asdf:**

```bash
# Install asdf plugin
asdf plugin add ruby

# Install Ruby
asdf install ruby 3.3.0
asdf global ruby 3.3.0

# Create .tool-versions
echo "ruby 3.3.0" > .tool-versions
```

### Step 2: Initialize Project

**Non-Rails Project:**

```bash
mkdir my-project && cd my-project

# Create Gemfile
bundle init

# Edit Gemfile
cat << 'EOF' > Gemfile
source 'https://rubygems.org'

ruby '3.3.0'

# Core gems
gem 'dotenv'
gem 'zeitwerk'

# Development
group :development, :test do
  gem 'rspec'
  gem 'rubocop'
  gem 'rubocop-rspec'
  gem 'pry'
end
EOF

# Install gems
bundle install
```

**Rails Project:**

```bash
# Install Rails
gem install rails

# Create new project
rails new my-app --database=postgresql --skip-test --api

# Or with specific options
rails new my-app \
  --database=postgresql \
  --skip-action-mailer \
  --skip-action-mailbox \
  --skip-action-text \
  --skip-active-storage \
  --skip-action-cable \
  --skip-asset-pipeline \
  --skip-javascript \
  --api
```

### Step 3: Project Structure

**Non-Rails:**

```
my-project/
├── Gemfile
├── Gemfile.lock
├── README.md
├── .ruby-version
├── .rubocop.yml
├── .rspec
├── .env.example
├── bin/
│   └── console           # Interactive console
├── lib/
│   ├── my_project.rb     # Main entry point
│   └── my_project/
│       ├── version.rb
│       ├── config.rb
│       └── services/
├── spec/
│   ├── spec_helper.rb
│   └── my_project/
└── config/
    └── boot.rb           # Bootstrapping
```

**Rails API:**

```
my-app/
├── Gemfile
├── Gemfile.lock
├── config/
│   ├── application.rb
│   ├── database.yml
│   ├── routes.rb
│   └── environments/
├── app/
│   ├── controllers/
│   ├── models/
│   ├── services/         # Business logic
│   ├── serializers/      # JSON serialization
│   └── jobs/
├── db/
│   ├── migrate/
│   └── schema.rb
├── spec/
└── lib/
```

### Step 4: Configuration

**config/boot.rb:**

```ruby
require 'bundler/setup'
require 'dotenv/load'
require 'zeitwerk'

loader = Zeitwerk::Loader.new
loader.push_dir(File.expand_path('../lib', __dir__))
loader.setup

module MyProject
  class Error < StandardError; end

  class << self
    def root
      @root ||= Pathname.new(File.expand_path('..', __dir__))
    end

    def env
      @env ||= ENV.fetch('RUBY_ENV', 'development')
    end

    def config
      @config ||= Config.new
    end
  end
end
```

**lib/my_project/config.rb:**

```ruby
module MyProject
  class Config
    def database_url
      ENV.fetch('DATABASE_URL')
    end

    def redis_url
      ENV.fetch('REDIS_URL', 'redis://localhost:6379')
    end

    def api_key
      ENV.fetch('API_KEY')
    end

    def development?
      MyProject.env == 'development'
    end

    def production?
      MyProject.env == 'production'
    end
  end
end
```

### Step 5: Bundler Best Practices

**Gemfile:**

```ruby
source 'https://rubygems.org'

ruby '3.3.0'

# Pin major versions for stability
gem 'pg', '~> 1.5'
gem 'redis', '~> 5.0'
gem 'sidekiq', '~> 7.0'

# Use specific version for critical gems
gem 'rails', '7.1.3'

# Group dependencies
group :development, :test do
  gem 'rspec-rails', '~> 6.0'
  gem 'factory_bot_rails'
  gem 'faker'
  gem 'pry-rails'
end

group :development do
  gem 'rubocop', require: false
  gem 'rubocop-rails', require: false
  gem 'rubocop-rspec', require: false
end

group :test do
  gem 'shoulda-matchers'
  gem 'webmock'
  gem 'vcr'
end

group :production do
  gem 'lograge'
end
```

**Bundle commands:**

```bash
# Install with locked versions
bundle install

# Update specific gem
bundle update sidekiq

# Update all gems
bundle update

# Check for security vulnerabilities
bundle audit

# Show outdated gems
bundle outdated
```

### Step 6: RuboCop Configuration

**.rubocop.yml:**

```yaml
require:
  - rubocop-rails
  - rubocop-rspec

AllCops:
  NewCops: enable
  TargetRubyVersion: 3.3
  Exclude:
    - 'db/schema.rb'
    - 'db/migrate/*.rb'
    - 'vendor/**/*'
    - 'bin/*'
    - 'node_modules/**/*'

Style/Documentation:
  Enabled: false

Style/FrozenStringLiteralComment:
  Enabled: true
  EnforcedStyle: always

Metrics/BlockLength:
  Exclude:
    - 'spec/**/*'
    - 'config/routes.rb'

Layout/LineLength:
  Max: 120

RSpec/ExampleLength:
  Max: 20

RSpec/MultipleExpectations:
  Max: 5
```

---

## Templates

### Console Script

**bin/console:**

```ruby
#!/usr/bin/env ruby

require_relative '../config/boot'
require 'pry'

Pry.start
```

### .env.example

```
# Database
DATABASE_URL=postgres://localhost/my_project_development

# Redis
REDIS_URL=redis://localhost:6379

# API Keys
API_KEY=your_api_key_here

# Environment
RUBY_ENV=development
```

### .gitignore

```
# Bundler
/.bundle
/vendor/bundle

# Environment
.env
.env.local
.env.*.local

# IDE
.idea/
*.swp
*.swo

# Logs
/log/*
!/log/.keep

# Temp files
/tmp/*
!/tmp/.keep

# Coverage
/coverage/

# OS
.DS_Store
```

---

## Examples

### Simple CLI Application

```ruby
# lib/my_cli.rb
require 'optparse'

module MyCLI
  class Runner
    def initialize(args)
      @options = parse_options(args)
    end

    def run
      puts "Hello, #{@options[:name]}!"
    end

    private

    def parse_options(args)
      options = { name: 'World' }

      OptionParser.new do |opts|
        opts.banner = 'Usage: my_cli [options]'

        opts.on('-n', '--name NAME', 'Name to greet') do |name|
          options[:name] = name
        end
      end.parse!(args)

      options
    end
  end
end

# bin/my_cli
#!/usr/bin/env ruby
require_relative '../lib/my_cli'
MyCLI::Runner.new(ARGV).run
```

---

## Common Mistakes

1. **Not committing Gemfile.lock** - Always commit for reproducible builds
2. **Using system Ruby** - Use version manager
3. **Not grouping gems** - Separate dev/test/production
4. **Ignoring bundle audit** - Check security regularly
5. **Missing .ruby-version** - Include for CI/CD

---

## Checklist

- [ ] Ruby version manager installed (rbenv/asdf)
- [ ] .ruby-version or .tool-versions created
- [ ] Gemfile with proper grouping
- [ ] Gemfile.lock committed
- [ ] RuboCop configured
- [ ] .env.example created
- [ ] .gitignore complete

---

## Next Steps

- M-RB-002: Ruby on Rails Patterns
- M-RB-003: Ruby Testing with RSpec
- M-RB-004: Ruby Code Quality

---

*Methodology M-RB-001 v1.0*
