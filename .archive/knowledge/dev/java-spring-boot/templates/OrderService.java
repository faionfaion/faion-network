// purpose: Service with @Transactional placement + entity↔DTO mapping
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~500 tokens when loaded as context

package com.example.order.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.order.domain.Order;
import com.example.order.domain.OrderRepository;
import com.example.order.dto.OrderRequest;
import com.example.order.dto.OrderResponse;

@Service
public class OrderService {

    private final OrderRepository repo;

    public OrderService(OrderRepository repo) {
        this.repo = repo;
    }

    @Transactional
    public OrderResponse create(OrderRequest req) {
        Order order = new Order(req.customer(), req.items());
        repo.save(order);
        return OrderResponse.from(order);
    }

    @Transactional(readOnly = true)
    public OrderResponse get(String id) {
        return repo.findWithItemsById(id)
                   .map(OrderResponse::from)
                   .orElseThrow(() -> new OrderNotFoundException(id));
    }
}
