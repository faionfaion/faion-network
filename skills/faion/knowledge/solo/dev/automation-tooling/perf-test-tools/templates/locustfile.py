"""locustfile.py — Locust load test starter with weighted tasks and auth.
Run: locust -f locustfile.py --host=https://api.example.com
Headless: locust -f locustfile.py --headless -u 100 -r 10 -t 5m
"""
import json
import random
from locust import HttpUser, task, between, events


class WebsiteUser(HttpUser):
    """Simulates typical user behavior."""

    wait_time = between(1, 5)  # realistic think time
    host = "https://api.example.com"

    def on_start(self):
        """Login and cache auth token."""
        response = self.client.post("/auth/login", json={
            "email": f"user{random.randint(1, 1000)}@example.com",
            "password": "testpassword",
        })
        self.headers = {}
        if response.status_code == 200:
            self.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

    @task(10)
    def browse_products(self):
        self.client.get("/api/products", headers=self.headers)

    @task(5)
    def view_product_detail(self):
        product_id = random.randint(1, 100)
        self.client.get(f"/api/products/{product_id}", headers=self.headers)

    @task(3)
    def search_products(self):
        terms = ["laptop", "phone", "tablet"]
        self.client.get(f"/api/products/search?q={random.choice(terms)}", headers=self.headers)

    @task(1)
    def add_to_cart(self):
        self.client.post("/api/cart/items", json={
            "product_id": random.randint(1, 100),
            "quantity": 1,
        }, headers=self.headers)


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, **kwargs):
    """Log slow requests for investigation."""
    if response_time > 2000:
        print(f"SLOW: {name} {response_time}ms")
