// purpose: Decorator composition Retry(Breaker(Call)) with fallback enqueue
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~450 tokens when loaded as context

package com.example.payment;

import java.time.Duration;
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.decorators.Decorators;
import io.github.resilience4j.retry.Retry;
import io.github.resilience4j.retry.RetryConfig;
import io.vavr.control.Try;
import org.springframework.stereotype.Service;

@Service
public class PaymentService {

    private final PaymentGatewayClient client;
    private final CircuitBreaker breaker;
    private final ChargeQueue queue;
    private final Retry retry;

    public PaymentService(PaymentGatewayClient client, CircuitBreaker paymentGatewayBreaker, ChargeQueue queue) {
        this.client = client;
        this.breaker = paymentGatewayBreaker;
        this.queue = queue;
        this.retry = Retry.of("payment-retry", RetryConfig.custom()
            .maxAttempts(3)
            .waitDuration(Duration.ofMillis(200))
            .build());
    }

    public ChargeResult charge(ChargeRequest req) {
        return Try.ofSupplier(Decorators.ofSupplier(() -> client.charge(req))
                .withCircuitBreaker(breaker)
                .withRetry(retry)
                .decorate())
            .recover(ex -> queue.enqueueForRetry(req))
            .get();
    }
}
