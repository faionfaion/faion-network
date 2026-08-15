// purpose: Typed @ConfigurationProperties record with Jakarta Bean Validation
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~300 tokens when loaded as context

package com.example.config;

import jakarta.validation.constraints.*;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

@Validated
@ConfigurationProperties(prefix = "app.mail")
public record MailProperties(
        @NotBlank String host,
        @Min(1) @Max(65535) int port,
        @NotBlank String user,
        String password,
        @NotBlank @Email String from,
        @Min(0) int maxRetries,
        @Min(100) int timeoutMs,
        boolean tlsEnabled
) {}
