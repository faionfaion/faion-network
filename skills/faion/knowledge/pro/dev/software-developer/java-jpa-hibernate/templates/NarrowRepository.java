// purpose: narrow read/write repository interfaces per narrow-repo-interface rule
// consumes: Order + DTO projections
// produces: Spring Data interface segregated for read vs write
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~250 tokens when loaded as reference

package faion.infra.orders;

import faion.domain.orders.Order;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.NoRepositoryBean;
import org.springframework.data.repository.query.Param;

import java.util.Optional;
import java.util.UUID;

@NoRepositoryBean
public interface OrderRepository {

    Optional<Order> findById(UUID id);

    @Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.id = :id")
    Optional<Order> findByIdWithItems(@Param("id") UUID id);

    Page<OrderSummaryDto> findAllSummaries(Pageable pageable);

    Order save(Order order);

    void delete(Order order);
}

interface OrderRepositoryJpa extends OrderRepository, JpaRepository<Order, UUID> {

    @Override
    @EntityGraph(attributePaths = {"items"})
    Optional<Order> findByIdWithItems(@Param("id") UUID id);

    @Override
    @Query("SELECT new faion.infra.orders.OrderSummaryDto(o.id, o.customerName, o.total) FROM Order o")
    Page<OrderSummaryDto> findAllSummaries(Pageable pageable);
}

record OrderSummaryDto(UUID id, String customerName, java.math.BigDecimal total) {}
