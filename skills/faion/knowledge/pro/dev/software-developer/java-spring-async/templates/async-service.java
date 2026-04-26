// NotificationService.java — @Async service with CompletableFuture and fan-out.
// This bean must NOT be the same bean as the caller (no self-invocation).

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
    private final SmsService smsService;

    @Async("emailExecutor")
    public CompletableFuture<Void> sendOrderConfirmation(Order order) {
        log.info("Sending order confirmation for order: {}", order.getId());
        try {
            emailService.send(
                order.getUser().getEmail(),
                "Order Confirmation",
                "Your order #" + order.getId() + " has been confirmed."
            );
            return CompletableFuture.completedFuture(null);
        } catch (Exception e) {
            log.error("Failed to send order confirmation for {}", order.getId(), e);
            return CompletableFuture.failedFuture(e);
        }
    }

    @Async("taskExecutor")
    public CompletableFuture<Void> sendWelcomeNotifications(User user) {
        CompletableFuture<Void> emailFuture = CompletableFuture.runAsync(() ->
            emailService.send(user.getEmail(), "Welcome!", "Welcome, " + user.getName() + "!")
        );
        CompletableFuture<Void> smsFuture = CompletableFuture.runAsync(() ->
            smsService.send(user.getPhone(), "Welcome to our service!")
        );
        return CompletableFuture.allOf(emailFuture, smsFuture)
            .exceptionally(ex -> {
                log.error("Failed to send welcome notifications for user {}", user.getId(), ex);
                return null;
            });
    }
}
