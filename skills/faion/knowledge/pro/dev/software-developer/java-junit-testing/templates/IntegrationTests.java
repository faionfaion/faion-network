// purpose: @SpringBootTest end-to-end integration test skeleton with Testcontainers
// consumes: full application context + real DB
// produces: integration test class
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~250 tokens when loaded as reference

package faion.app;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class OrdersIntegrationTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

    @Autowired
    private TestRestTemplate rest;

    @Test
    void createAndGetOrder_endToEnd() {
        ResponseEntity<String> created = rest.postForEntity(
            "/api/orders",
            new CreateOrderRequest("Alice"),
            String.class
        );
        assertThat(created.getStatusCode()).isEqualTo(HttpStatus.CREATED);

        ResponseEntity<String> got = rest.getForEntity(created.getHeaders().getLocation(), String.class);
        assertThat(got.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(got.getBody()).contains("Alice");
    }

    record CreateOrderRequest(String customerName) {}
}
