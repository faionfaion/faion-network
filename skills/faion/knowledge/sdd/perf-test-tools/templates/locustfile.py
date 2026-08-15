# __faion_header_v1__
# purpose: Locust user class with weighted tasks + threshold check
# consumes: see content/02-output-contract.xml
# produces: code
# depends-on: content/02-output-contract.xml + content/01-core-rules.xml#tool-by-team-language
# token-budget-impact: ~190 tokens when loaded as context
# faion_header_json: {"__faion_header__":{"purpose":"Locust user class with weighted tasks + threshold check","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/02-output-contract.xml + content/01-core-rules.xml#tool-by-team-language","token_budget_impact":"~190 tokens when loaded as context"}}
from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(0.5, 2.0)

    @task(3)
    def checkout(self):
        self.client.get("/api/v1/checkout")

    @task(1)
    def search(self):
        self.client.get("/api/v1/search?q=hello")
