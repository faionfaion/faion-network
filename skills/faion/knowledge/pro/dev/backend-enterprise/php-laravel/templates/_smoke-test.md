<!-- purpose: minimum viable Laravel project structure reference for the umbrella -->
<!-- consumes: feature spec -->
<!-- produces: project layout conforming to queue-driver-not-sync-in-prod + scheduler-runs-via-supervisor -->
<!-- depends-on: content/01-core-rules.xml rules queue-driver-not-sync-in-prod, scheduler-runs-via-supervisor -->
<!-- token-budget-impact: ~300 tokens when loaded as context -->

# Smoke-test Laravel umbrella layout

```
app/
├── Actions/<Feature>/                  // see decomposition-laravel
├── Http/
│   ├── Controllers/                    // see php-laravel-patterns
│   ├── Requests/
│   └── Resources/
├── Jobs/                               // see php-laravel-queues
├── Models/                             // see php-eloquent
├── Services/
└── Console/Kernel.php                  // single scheduler entry

config/
├── queue.php                           // QUEUE_CONNECTION=redis in prod
└── horizon.php

deploy/supervisor/
├── laravel-worker.conf
└── laravel-scheduler.conf

tests/                                  // see php-phpunit-testing
├── Feature/
└── Unit/
```

Required env (prod):

```
APP_ENV=production
QUEUE_CONNECTION=redis
LOG_CHANNEL=stack
```
