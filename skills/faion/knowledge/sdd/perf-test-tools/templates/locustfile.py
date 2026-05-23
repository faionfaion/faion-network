# __faion_header_v1__
# purpose: Locust user class with weighted tasks + threshold check
# consumes: see content/02-output-contract.xml
# produces: code; depends-on: content/01-core-rules.xml#tool-by-team-language
# faion_header_json: {"__faion_header__":{"purpose":"Locust user class with weighted tasks + threshold check","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#tool-by-team-language","token_budget_impact":"~150 tokens when loaded"}}
from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(0.5, 2.0)

    @task(3)
    def checkout(self):
        self.client.get("/api/v1/checkout")

    @task(1)
    def search(self):
        self.client.get("/api/v1/search?q=hello")
