// purpose: Spring Boot service using constructor injection
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for practices-backend-languages
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

package com.example.orders;

import org.springframework.stereotype.Service;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;

    public Order create(CreateOrderDto dto) {
        Order order = Order.builder()
            .customerId(dto.getCustomerId())
            .amount(dto.getAmount())
            .build();
        return orderRepository.save(order);
    }
}
