# M-PHP-004: PHP Code Quality

## Metadata
- **Category:** Development/Backend/PHP
- **Difficulty:** Beginner
- **Tags:** #dev, #php, #quality, #phpstan, #methodology
- **Agent:** faion-code-agent

---

## Problem

PHP's dynamic typing and flexibility enable bugs that only appear at runtime. Without static analysis, type errors hide in production code. Style inconsistencies waste code review time.

## Promise

After this methodology, your PHP code will be type-safe, consistent, and secure. Static analysis will catch bugs before they reach production.

## Overview

Modern PHP quality uses PHPStan for static analysis, PHP-CS-Fixer for formatting, and security scanners for vulnerability detection.

---

## Framework

### Step 1: PHPStan Setup

**composer.json:**

```json
{
  "require-dev": {
    "phpstan/phpstan": "^1.10",
    "phpstan/phpstan-strict-rules": "^1.5",
    "nunomaduro/larastan": "^2.0"
  }
}
```

**phpstan.neon:**

```neon
includes:
    - vendor/nunomaduro/larastan/extension.neon
    - vendor/phpstan/phpstan-strict-rules/rules.neon

parameters:
    level: 8
    paths:
        - app
        - src
    excludePaths:
        - vendor
        - storage
        - bootstrap/cache
    checkMissingIterableValueType: true
    checkGenericClassInNonGenericObjectType: true
    reportUnmatchedIgnoredErrors: true
    ignoreErrors:
        # Add ignored errors here
        # - '#Call to an undefined method#'
```

**PHPStan levels:**

| Level | Description |
|-------|-------------|
| 0 | Basic checks |
| 1 | Unknown variables |
| 2 | Unknown methods/functions |
| 3 | Return types |
| 4 | Type casts |
| 5 | Argument types |
| 6 | Missing typehints |
| 7 | Union types |
| 8 | Mixed type |
| 9 | Everything (strictest) |

### Step 2: PHP-CS-Fixer

**composer.json:**

```json
{
  "require-dev": {
    "friendsofphp/php-cs-fixer": "^3.0"
  }
}
```

**.php-cs-fixer.php:**

```php
<?php

use PhpCsFixer\Config;
use PhpCsFixer\Finder;

$finder = Finder::create()
    ->in([
        __DIR__ . '/app',
        __DIR__ . '/config',
        __DIR__ . '/database',
        __DIR__ . '/routes',
        __DIR__ . '/tests',
    ])
    ->name('*.php')
    ->notName('*.blade.php')
    ->ignoreDotFiles(true)
    ->ignoreVCS(true);

return (new Config())
    ->setRules([
        '@PSR12' => true,
        '@PHP82Migration' => true,
        'array_syntax' => ['syntax' => 'short'],
        'binary_operator_spaces' => true,
        'blank_line_before_statement' => [
            'statements' => ['return', 'throw', 'try'],
        ],
        'cast_spaces' => ['space' => 'single'],
        'class_attributes_separation' => [
            'elements' => [
                'method' => 'one',
                'property' => 'one',
            ],
        ],
        'concat_space' => ['spacing' => 'one'],
        'declare_strict_types' => true,
        'final_class' => false,
        'fully_qualified_strict_types' => true,
        'global_namespace_import' => [
            'import_classes' => true,
            'import_constants' => true,
            'import_functions' => true,
        ],
        'method_argument_space' => [
            'on_multiline' => 'ensure_fully_multiline',
        ],
        'no_unused_imports' => true,
        'ordered_imports' => ['sort_algorithm' => 'alpha'],
        'single_quote' => true,
        'trailing_comma_in_multiline' => [
            'elements' => ['arrays', 'arguments', 'parameters'],
        ],
        'yoda_style' => false,
    ])
    ->setFinder($finder)
    ->setRiskyAllowed(true)
    ->setCacheFile(__DIR__ . '/.php-cs-fixer.cache');
```

### Step 3: Rector for Automated Refactoring

**composer.json:**

```json
{
  "require-dev": {
    "rector/rector": "^0.18"
  }
}
```

**rector.php:**

```php
<?php

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;
use Rector\Set\ValueObject\SetList;

return static function (RectorConfig $rectorConfig): void {
    $rectorConfig->paths([
        __DIR__ . '/app',
        __DIR__ . '/src',
    ]);

    $rectorConfig->sets([
        LevelSetList::UP_TO_PHP_83,
        SetList::CODE_QUALITY,
        SetList::DEAD_CODE,
        SetList::EARLY_RETURN,
        SetList::TYPE_DECLARATION,
    ]);

    $rectorConfig->skip([
        // Skip specific rules or paths
    ]);
};
```

### Step 4: Security Scanning

**Composer Security:**

```bash
# Check for known vulnerabilities
composer audit
```

**Psalm Security Analysis:**

```json
{
  "require-dev": {
    "vimeo/psalm": "^5.0",
    "psalm/plugin-laravel": "^2.0"
  }
}
```

**psalm.xml:**

```xml
<?xml version="1.0"?>
<psalm
    errorLevel="2"
    findUnusedVariablesAndParams="true"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="https://getpsalm.org/schema/config"
    xsi:schemaLocation="https://getpsalm.org/schema/config vendor/vimeo/psalm/config.xsd"
>
    <projectFiles>
        <directory name="app"/>
        <ignoreFiles>
            <directory name="vendor"/>
        </ignoreFiles>
    </projectFiles>
    <plugins>
        <pluginClass class="Psalm\LaravelPlugin\Plugin"/>
    </plugins>
    <issueHandlers>
        <TaintedInput errorLevel="error"/>
    </issueHandlers>
</psalm>
```

### Step 5: IDE Helper (Laravel)

```bash
composer require --dev barryvdh/laravel-ide-helper

# Generate helpers
php artisan ide-helper:generate
php artisan ide-helper:models --nowrite
php artisan ide-helper:meta
```

### Step 6: Automation

**Makefile:**

```makefile
.PHONY: lint fix test quality

lint:
	vendor/bin/php-cs-fixer fix --dry-run --diff
	vendor/bin/phpstan analyse

fix:
	vendor/bin/php-cs-fixer fix
	vendor/bin/rector process

test:
	vendor/bin/phpunit

security:
	composer audit

quality: lint security test
	@echo "All quality checks passed!"
```

**composer.json scripts:**

```json
{
  "scripts": {
    "lint": "php-cs-fixer fix --dry-run --diff && phpstan analyse",
    "fix": "php-cs-fixer fix && rector process",
    "test": "phpunit",
    "quality": ["@lint", "@test"]
  }
}
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

      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          tools: composer:v2

      - name: Install dependencies
        run: composer install --no-interaction

      - name: PHP-CS-Fixer
        run: vendor/bin/php-cs-fixer fix --dry-run --diff

      - name: PHPStan
        run: vendor/bin/phpstan analyse

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'

      - name: Security audit
        run: composer audit

  test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: testing
        ports:
          - 3306:3306

    steps:
      - uses: actions/checkout@v4

      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          coverage: xdebug

      - name: Install dependencies
        run: composer install --no-interaction

      - name: Run tests
        run: vendor/bin/phpunit --coverage-text
        env:
          DB_CONNECTION: mysql
          DB_HOST: 127.0.0.1
          DB_DATABASE: testing
          DB_USERNAME: root
          DB_PASSWORD: root
```

### Pre-commit Hook

**.git/hooks/pre-commit:**

```bash
#!/bin/sh

FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.php$')

if [ -n "$FILES" ]; then
    # Check style
    vendor/bin/php-cs-fixer fix --dry-run --diff $FILES
    if [ $? -ne 0 ]; then
        echo "Code style issues found. Run: composer fix"
        exit 1
    fi

    # Static analysis
    vendor/bin/phpstan analyse $FILES
    if [ $? -ne 0 ]; then
        echo "Static analysis failed."
        exit 1
    fi
fi

exit 0
```

---

## Examples

### Type Annotations

```php
<?php

declare(strict_types=1);

namespace App\Services;

use App\Models\User;
use App\Data\UserData;

class UserService
{
    /**
     * @param array<string, mixed> $filters
     * @return array<User>
     */
    public function search(array $filters): array
    {
        // ...
    }

    /**
     * @throws UserNotFoundException
     */
    public function findOrFail(int $id): User
    {
        $user = User::find($id);

        if ($user === null) {
            throw new UserNotFoundException("User {$id} not found");
        }

        return $user;
    }
}
```

---

## Common Mistakes

1. **Low PHPStan level** - Aim for level 8+
2. **Ignoring errors** - Fix issues, don't suppress them
3. **No CI enforcement** - Quality checks must block merges
4. **Missing strict_types** - Add to every PHP file
5. **No security audits** - Run composer audit regularly

---

## Checklist

- [ ] PHPStan at level 8+
- [ ] PHP-CS-Fixer configured
- [ ] Rector for upgrades (optional)
- [ ] Security scanning enabled
- [ ] IDE helpers generated
- [ ] CI runs all checks
- [ ] Pre-commit hooks installed
- [ ] strict_types everywhere

---

## Next Steps

- M-PHP-001: PHP Project Setup
- M-PHP-003: PHP Testing with PHPUnit
- M-DO-001: CI/CD with GitHub Actions

---

*Methodology M-PHP-004 v1.0*
