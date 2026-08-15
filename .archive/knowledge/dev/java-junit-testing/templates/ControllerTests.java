// purpose: @WebMvcTest controller test skeleton
// consumes: controller class + service mock
// produces: controller test class
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~250 tokens when loaded as reference

package faion.web;

import com.fasterxml.jackson.databind.ObjectMapper;
import faion.app.orders.OrderService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(OrdersController.class)
class OrdersControllerTest {

    @Autowired private MockMvc mvc;
    @Autowired private ObjectMapper mapper;
    @MockBean private OrderService service;

    @Test
    void getById_existingOrder_returns200() throws Exception {
        when(service.getById(eq(java.util.UUID.fromString("00000000-0000-0000-0000-000000000001"))))
            .thenReturn(new OrderResponse("00000000-0000-0000-0000-000000000001", "Alice", "10.00"));

        mvc.perform(get("/api/orders/00000000-0000-0000-0000-000000000001"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.customerName").value("Alice"));
    }

    @ParameterizedTest
    @ValueSource(strings = {"not-a-uuid", "00000000-0000-0000-0000-0000000000XX"})
    void getById_invalidUuid_returns400(String id) throws Exception {
        mvc.perform(get("/api/orders/" + id))
            .andExpect(status().isBadRequest());
    }

    record OrderResponse(String id, String customerName, String total) {}
}
