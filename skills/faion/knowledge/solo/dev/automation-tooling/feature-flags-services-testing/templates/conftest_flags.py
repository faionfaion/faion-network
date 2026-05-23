# __faion_header_v1__
# purpose: pytest fixtures that exercise ON and OFF branches
# consumes: see content/02-output-contract.xml
# produces: spec; depends-on: content/01-core-rules.xml#test-both-branches
# faion_header_json: {"__faion_header__":{"purpose":"pytest fixtures that exercise ON and OFF branches","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#test-both-branches","token_budget_impact":"~150 tokens when loaded"}}
import pytest


@pytest.fixture
def flag_on(monkeypatch):
    def _on(name: str) -> None:
        monkeypatch.setenv(f"FF_{name.upper().replace('-', '_')}", "true")
    return _on


@pytest.fixture
def flag_off(monkeypatch):
    def _off(name: str) -> None:
        monkeypatch.setenv(f"FF_{name.upper().replace('-', '_')}", "false")
    return _off
