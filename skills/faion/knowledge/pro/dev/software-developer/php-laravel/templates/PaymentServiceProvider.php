// purpose: Service Provider binding contracts to implementations
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~300 tokens when loaded as context

<?php

namespace App\Providers;

use App\Contracts\MailService;
use App\Contracts\CacheService;
use App\Services\SendgridMailService;
use App\Services\RedisCacheService;
use Illuminate\Support\ServiceProvider;

class PaymentServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->bind(MailService::class, SendgridMailService::class);
        $this->app->bind(CacheService::class, RedisCacheService::class);
    }

    public function boot(): void
    {
        // Macros, route model bindings, blade directives go here — not env() or DB queries.
    }
}
