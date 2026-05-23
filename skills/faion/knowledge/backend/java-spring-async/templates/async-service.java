// purpose: service method skeleton returning CompletableFuture<T> with @Async("emailExecutor")
// consumes: workload SLA + executor name from AsyncConfig
// produces: async service method conforming to completablefuture-return rule
// depends-on: content/01-core-rules.xml rules named-executor, completablefuture-return
// token-budget-impact: ~300 tokens when loaded as context
// @Async service method skeleton — returns CompletableFuture<Void>
// Replace: NotificationService, emailExecutor, EmailService, Order

package com.example.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;

@Service
@RequiredArgsConstructor
@Slf4j
public class NotificationService {

    private final EmailService emailService;

    /**
     * Sends order confirmation email asynchronously on the "emailExecutor" pool.
     * Returns CompletableFuture<Void> — callers can chain or await.
     *
     * @param order the order to confirm (pass ID in production — re-fetch here)
     * @return completed future on success, failed future on error
     */
    @Async("emailExecutor")
    public CompletableFuture<Void> sendOrderConfirmation(Order order) {
        log.info("Sending order confirmation for order {}", order.getId());
        try {
            emailService.send(
                order.getUser().getEmail(),
                "Order Confirmation #" + order.getId(),
                buildEmailBody(order)
            );
            return CompletableFuture.completedFuture(null);
        } catch (Exception e) {
            log.error("Failed to send confirmation for order {}", order.getId(), e);
            return CompletableFuture.failedFuture(e);
        }
    }

    private String buildEmailBody(Order order) {
        return "Your order #" + order.getId() + " has been confirmed.";
    }
}
