// purpose: thin @RestController skeleton conforming to thin-controller rule
// consumes: OrdersService + request DTO
// produces: HTTP controller artefact
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~300 tokens when loaded as reference

package faion.web.orders;

import faion.app.orders.OrdersService;
import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/orders")
public class OrdersController {

    private final OrdersService service;

    public OrdersController(OrdersService service) {
        this.service = service;
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrderResponse> getById(@PathVariable UUID id) {
        return ResponseEntity.ok(service.getById(id));
    }

    @GetMapping
    public Page<OrderSummary> list(Pageable pageable) {
        return service.list(pageable);
    }

    @PostMapping
    public ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) {
        OrderResponse created = service.create(req);
        return ResponseEntity.created(java.net.URI.create("/api/orders/" + created.id())).body(created);
    }
}
