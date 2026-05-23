// purpose: Mockito service unit test skeleton
// consumes: service + repository mock
// produces: service unit test class
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200 tokens when loaded as reference

package faion.app.orders;

import faion.infra.orders.OrderRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock private OrderRepository repository;
    @InjectMocks private OrderService service;

    @Test
    void getById_existingOrder_returnsResponse() {
        UUID id = UUID.randomUUID();
        when(repository.findByIdWithItems(id)).thenReturn(Optional.of(new faion.domain.orders.Order("Alice")));

        OrderResponse response = service.getById(id);

        assertThat(response.customerName()).isEqualTo("Alice");
        verify(repository).findByIdWithItems(argThat(arg -> arg.equals(id)));
    }

    @Test
    void getById_missing_throws() {
        UUID id = UUID.randomUUID();
        when(repository.findByIdWithItems(id)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> service.getById(id))
            .isInstanceOf(OrderNotFoundException.class);
    }
}
