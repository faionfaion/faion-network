// purpose: transactional service returning DTOs (not entities)
// consumes: OrderRepository + request inputs
// produces: service class for the controller
// depends-on: content/01-core-rules.xml, templates/NarrowRepository.java
// token-budget-impact: ~250 tokens when loaded as reference

package faion.app.orders;

import faion.domain.orders.Order;
import faion.infra.orders.OrderRepository;
import faion.infra.orders.OrderSummaryDto;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
@Transactional(readOnly = true)
public class OrderService {

    private final OrderRepository repository;

    public OrderService(OrderRepository repository) {
        this.repository = repository;
    }

    public OrderResponse getById(UUID id) {
        Order order = repository.findByIdWithItems(id)
            .orElseThrow(() -> new OrderNotFoundException(id));
        return OrderResponse.from(order);
    }

    public Page<OrderSummaryDto> list(Pageable pageable) {
        return repository.findAllSummaries(pageable);
    }

    @Transactional
    public OrderResponse create(CreateOrderRequest req) {
        Order order = new Order(req.customerName());
        repository.save(order);
        return OrderResponse.from(order);
    }
}

record CreateOrderRequest(String customerName) {}
record OrderResponse(UUID id, String customerName, java.math.BigDecimal total) {
    static OrderResponse from(Order o) {
        return new OrderResponse(o.getId(), o.getCustomerName(), o.getTotal());
    }
}

class OrderNotFoundException extends RuntimeException {
    OrderNotFoundException(UUID id) { super("order not found: " + id); }
}
