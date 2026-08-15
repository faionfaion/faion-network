// purpose: JPA entity with audit timestamps + version + justified associations
// consumes: entity field spec
// produces: Hibernate entity class
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~300 tokens when loaded as reference

package faion.domain.orders;

import jakarta.persistence.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, length = 200)
    private String customerName;

    @Column(nullable = false, precision = 18, scale = 2)
    private BigDecimal total = BigDecimal.ZERO;

    /**
     * Items are wholly owned by Order. Cascade PERSIST + orphanRemoval so the
     * aggregate boundary matches persistence. Fetch LAZY by default; loaded
     * eagerly only via JOIN FETCH where required.
     */
    @OneToMany(mappedBy = "order", cascade = {CascadeType.PERSIST, CascadeType.MERGE}, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    @Version
    private Long version;

    @CreationTimestamp
    @Column(updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    private Instant updatedAt;

    protected Order() { }

    public Order(String customerName) {
        this.customerName = customerName;
    }

    public UUID getId() { return id; }
    public String getCustomerName() { return customerName; }
    public BigDecimal getTotal() { return total; }
    public List<OrderItem> getItems() { return List.copyOf(items); }
    public Long getVersion() { return version; }
}
