"""
purpose: FastAPI service skeleton with circuit-breaker import + DB ownership.
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (microservices-design)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from fastapi import FastAPI
from .infra.circuit_breaker import CircuitBreaker
from .infra.db import owned_db_session

app = FastAPI(title="orders-service")

_payment_breaker = CircuitBreaker(failure_threshold=5, reset_after_sec=30)


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    async with owned_db_session() as db:
        # only this service writes to this DB
        return await db.fetch_one("SELECT id, status FROM orders WHERE id = $1", order_id)


@app.post("/orders/{order_id}/charge")
async def charge(order_id: str):
    return await _payment_breaker.call(_charge_payment, order_id)


async def _charge_payment(order_id: str):
    # HTTP call to payments service; never import payments code directly
    ...
