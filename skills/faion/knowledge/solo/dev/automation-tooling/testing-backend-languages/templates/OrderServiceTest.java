// purpose: Spring service unit test using MockitoExtension (no SpringBootTest)
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for testing-backend-languages
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

package com.example.orders;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock OrderRepository repo;
    @InjectMocks OrderService svc;

    @Test
    void charge_persists_charged_status() {
        Order o = Order.builder().amount(1000).build();
        when(repo.save(o)).thenReturn(o);
        Order result = svc.charge(o);
        assertThat(result.getStatus()).isEqualTo("charged");
    }
}
