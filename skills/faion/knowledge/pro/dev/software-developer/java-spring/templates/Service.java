// purpose: @Transactional service skeleton returning DTOs only
// consumes: OrderRepository (narrow) + DTOs
// produces: service class for the controller
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~300 tokens when loaded as reference

package faion.app.orders;

import faion.infra.orders.OrderRepository;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.UUID;

@Service
@Transactional(readOnly = true)
public class OrdersService {

    private final OrderRepository repository;

    public OrdersService(OrderRepository repository) {
        this.repository = repository;
    }

    public OrderResponse getById(UUID id) {
        return repository.findByIdWithItems(id)
            .map(OrderResponse::from)
            .orElseThrow(() -> new OrderNotFoundException(id));
    }

    public Page<OrderSummary> list(Pageable pageable) {
        return repository.findAllSummaries(pageable);
    }

    @Transactional
    public OrderResponse create(CreateOrderRequest req) {
        var saved = repository.save(new faion.domain.orders.Order(req.customerName()));
        return OrderResponse.from(saved);
    }
}

record CreateOrderRequest(
    @NotBlank @Size(max = 200) String customerName,
    @Positive BigDecimal total
) {}

record OrderResponse(UUID id, String customerName, BigDecimal total) {
    static OrderResponse from(faion.domain.orders.Order o) {
        return new OrderResponse(o.getId(), o.getCustomerName(), o.getTotal());
    }
}

record OrderSummary(UUID id, String customerName, BigDecimal total) {}

class OrderNotFoundException extends RuntimeException {
    OrderNotFoundException(UUID id) { super("order not found: " + id); }
}
