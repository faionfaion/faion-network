// purpose: Temporal workflow skeleton with reverse-order compensations
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~500 tokens when loaded as context

package com.example.saga;

import io.temporal.activity.ActivityOptions;
import io.temporal.workflow.Workflow;
import io.temporal.workflow.WorkflowInterface;
import io.temporal.workflow.WorkflowMethod;
import java.time.Duration;

@WorkflowInterface
public interface OrderSagaWorkflow {

    @WorkflowMethod
    OrderResult placeOrder(OrderRequest req);
}

public class OrderSagaWorkflowImpl implements OrderSagaWorkflow {

    private final OrderActivities order = Workflow.newActivityStub(OrderActivities.class,
        ActivityOptions.newBuilder().setStartToCloseTimeout(Duration.ofSeconds(10)).build());
    private final BillingActivities billing = Workflow.newActivityStub(BillingActivities.class,
        ActivityOptions.newBuilder().setStartToCloseTimeout(Duration.ofSeconds(10)).build());
    private final InventoryActivities inventory = Workflow.newActivityStub(InventoryActivities.class,
        ActivityOptions.newBuilder().setStartToCloseTimeout(Duration.ofSeconds(10)).build());
    private final ShippingActivities shipping = Workflow.newActivityStub(ShippingActivities.class,
        ActivityOptions.newBuilder().setStartToCloseTimeout(Duration.ofSeconds(10)).build());

    @Override
    public OrderResult placeOrder(OrderRequest req) {
        String sagaId = Workflow.randomUUID().toString();
        String orderId = order.createPending(req, sagaId);
        try {
            String chargeId = billing.charge(req, sagaId);
            try {
                String reservationId = inventory.reserve(req, sagaId);
                try {
                    shipping.schedulePickup(req, sagaId);
                    return new OrderResult(orderId, "confirmed");
                } catch (Exception e) {
                    inventory.releaseStock(reservationId, sagaId);
                    billing.refundCard(chargeId, sagaId);
                    order.cancelOrder(orderId, sagaId);
                    throw Workflow.wrap(e);
                }
            } catch (Exception e) {
                billing.refundCard(chargeId, sagaId);
                order.cancelOrder(orderId, sagaId);
                throw Workflow.wrap(e);
            }
        } catch (Exception e) {
            order.cancelOrder(orderId, sagaId);
            throw Workflow.wrap(e);
        }
    }
}
