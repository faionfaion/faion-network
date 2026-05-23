// purpose: @Async service returning CompletableFuture with fan-out pattern
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~500 tokens when loaded as context

package com.example.service;

import java.util.concurrent.CompletableFuture;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

@Service
public class NotificationService {

    private static final Logger log = LoggerFactory.getLogger(NotificationService.class);
    private final EmailService emailService;
    private final SmsService smsService;

    public NotificationService(EmailService emailService, SmsService smsService) {
        this.emailService = emailService;
        this.smsService = smsService;
    }

    @Async("taskExecutor")
    public CompletableFuture<Void> sendOrderConfirmation(Order order) {
        try {
            emailService.send(order.userEmail(), "Order Confirmation", "Order #" + order.id() + " confirmed.");
            return CompletableFuture.completedFuture(null);
        } catch (Exception e) {
            log.error("Failed to send order confirmation {}", order.id(), e);
            return CompletableFuture.failedFuture(e);
        }
    }

    @Async("taskExecutor")
    public CompletableFuture<Void> sendWelcome(User user) {
        CompletableFuture<Void> email = CompletableFuture.runAsync(() ->
            emailService.send(user.email(), "Welcome!", "Welcome, " + user.name() + "!"));
        CompletableFuture<Void> sms = CompletableFuture.runAsync(() ->
            smsService.send(user.phone(), "Welcome to our service!"));
        return CompletableFuture.allOf(email, sms)
            .exceptionally(ex -> { log.error("Welcome notifications failed for {}", user.id(), ex); return null; });
    }
}
