# M-PHP-001: PHP Project Setup with Composer

## Metadata
- **Category:** Development/Backend/PHP
- **Difficulty:** Beginner
- **Tags:** #dev, #php, #backend, #composer, #methodology
- **Agent:** faion-code-agent

---

## Problem

PHP projects without proper structure become hard to maintain. Autoloading, dependency management, and environment configuration require careful setup. You need a modern PHP foundation.

## Promise

After this methodology, you will have a professional PHP project with Composer, PSR-4 autoloading, and proper structure that follows modern PHP best practices.

## Overview

Modern PHP (8.2+) uses Composer for dependencies, PSR-4 for autoloading, and follows community standards. This methodology covers setup for both Laravel and vanilla PHP projects.

---

## Framework

### Step 1: PHP Version Management

```bash
# Check version
php -v

# Install specific version (Ubuntu/Debian)
sudo add-apt-repository ppa:ondrej/php
sudo apt install php8.3 php8.3-cli php8.3-mbstring php8.3-xml php8.3-curl

# Install Composer
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer

# Verify
composer --version
```

### Step 2: Initialize Project

**Vanilla PHP:**

```bash
mkdir my-project && cd my-project

# Initialize Composer
composer init

# Or create with type
composer init --name="vendor/my-project" --type="project"
```

**Laravel:**

```bash
# Create new Laravel project
composer create-project laravel/laravel my-app

# Or with installer
composer global require laravel/installer
laravel new my-app
```

### Step 3: Project Structure

**Vanilla PHP:**

```
my-project/
├── composer.json
├── composer.lock
├── README.md
├── .env.example
├── .gitignore
├── bin/
│   └── console               # CLI entry point
├── config/
│   ├── app.php
│   └── database.php
├── public/
│   └── index.php             # Web entry point
├── src/
│   ├── App.php
│   ├── Config/
│   ├── Controller/
│   ├── Service/
│   ├── Repository/
│   └── Entity/
├── tests/
│   ├── Unit/
│   └── Integration/
├── var/
│   ├── cache/
│   └── log/
└── vendor/                   # Gitignored
```

### Step 4: Composer Configuration

**composer.json:**

```json
{
  "name": "vendor/my-project",
  "description": "My PHP project",
  "type": "project",
  "license": "MIT",
  "require": {
    "php": "^8.2",
    "vlucas/phpdotenv": "^5.5",
    "monolog/monolog": "^3.0"
  },
  "require-dev": {
    "phpunit/phpunit": "^10.0",
    "phpstan/phpstan": "^1.10",
    "squizlabs/php_codesniffer": "^3.7",
    "friendsofphp/php-cs-fixer": "^3.0"
  },
  "autoload": {
    "psr-4": {
      "App\\": "src/"
    }
  },
  "autoload-dev": {
    "psr-4": {
      "Tests\\": "tests/"
    }
  },
  "scripts": {
    "test": "phpunit",
    "stan": "phpstan analyse src",
    "cs": "php-cs-fixer fix --dry-run --diff",
    "cs-fix": "php-cs-fixer fix",
    "quality": ["@stan", "@cs", "@test"]
  },
  "config": {
    "sort-packages": true,
    "optimize-autoloader": true
  }
}
```

### Step 5: Entry Points

**public/index.php:**

```php
<?php

declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

use App\App;
use App\Config\Config;

// Load environment
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/..');
$dotenv->load();

// Bootstrap application
$config = Config::load();
$app = new App($config);

// Run
$app->run();
```

**bin/console:**

```php
#!/usr/bin/env php
<?php

declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

use App\Console\Application;

$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/..');
$dotenv->load();

$app = new Application();
$app->run();
```

### Step 6: Configuration

**src/Config/Config.php:**

```php
<?php

declare(strict_types=1);

namespace App\Config;

class Config
{
    private array $config;

    public function __construct(array $config)
    {
        $this->config = $config;
    }

    public static function load(): self
    {
        return new self([
            'app' => [
                'name' => self::env('APP_NAME', 'My App'),
                'env' => self::env('APP_ENV', 'development'),
                'debug' => self::env('APP_DEBUG', 'false') === 'true',
            ],
            'database' => [
                'driver' => self::env('DB_DRIVER', 'mysql'),
                'host' => self::env('DB_HOST', 'localhost'),
                'port' => (int) self::env('DB_PORT', '3306'),
                'database' => self::env('DB_DATABASE'),
                'username' => self::env('DB_USERNAME'),
                'password' => self::env('DB_PASSWORD'),
            ],
        ]);
    }

    public function get(string $key, mixed $default = null): mixed
    {
        $keys = explode('.', $key);
        $value = $this->config;

        foreach ($keys as $k) {
            if (!isset($value[$k])) {
                return $default;
            }
            $value = $value[$k];
        }

        return $value;
    }

    private static function env(string $key, ?string $default = null): ?string
    {
        $value = $_ENV[$key] ?? getenv($key);
        return $value !== false ? $value : $default;
    }
}
```

---

## Templates

**.env.example:**

```
APP_NAME="My App"
APP_ENV=development
APP_DEBUG=true

DB_DRIVER=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=myapp
DB_USERNAME=root
DB_PASSWORD=

LOG_LEVEL=debug
```

**.gitignore:**

```
/vendor/
/.env
/var/cache/*
/var/log/*
!var/cache/.gitkeep
!var/log/.gitkeep
.phpunit.result.cache
.php-cs-fixer.cache
composer.phar
```

**Dockerfile:**

```dockerfile
FROM php:8.3-fpm-alpine

WORKDIR /app

# Install extensions
RUN docker-php-ext-install pdo pdo_mysql

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Copy application
COPY composer.json composer.lock ./
RUN composer install --no-dev --optimize-autoloader

COPY . .

EXPOSE 9000
CMD ["php-fpm"]
```

---

## Examples

### Simple API Application

```php
<?php
// src/App.php

declare(strict_types=1);

namespace App;

use App\Config\Config;
use App\Controller\HealthController;

class App
{
    public function __construct(private Config $config) {}

    public function run(): void
    {
        $path = $_SERVER['REQUEST_URI'] ?? '/';
        $method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

        $response = $this->route($method, $path);

        header('Content-Type: application/json');
        http_response_code($response['status']);
        echo json_encode($response['body']);
    }

    private function route(string $method, string $path): array
    {
        return match (true) {
            $method === 'GET' && $path === '/health' => (new HealthController())->index(),
            default => ['status' => 404, 'body' => ['error' => 'Not Found']],
        };
    }
}
```

---

## Common Mistakes

1. **Not using strict_types** - Add `declare(strict_types=1)` to all files
2. **Ignoring composer.lock** - Always commit for reproducible builds
3. **Using global functions** - Use classes and dependency injection
4. **No autoloading** - Configure PSR-4 in composer.json
5. **Exposing .env** - Keep outside public directory

---

## Checklist

- [ ] PHP 8.2+ installed
- [ ] Composer initialized
- [ ] PSR-4 autoloading configured
- [ ] Environment variables with phpdotenv
- [ ] strict_types in all files
- [ ] .gitignore complete
- [ ] Development tools installed (PHPStan, PHP CS Fixer)

---

## Next Steps

- M-PHP-002: PHP Laravel Patterns
- M-PHP-003: PHP Testing with PHPUnit
- M-PHP-004: PHP Code Quality

---

*Methodology M-PHP-001 v1.0*
