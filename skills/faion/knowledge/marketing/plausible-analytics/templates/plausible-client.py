"""Plausible Stats API client — aggregate, timeseries, breakdown, realtime."""
import requests


class PlausibleClient:
    def __init__(self, api_key: str, site_id: str, base_url: str = "https://plausible.io"):
        self.site_id = site_id
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def aggregate(self, period: str = "30d", metrics: list[str] | None = None) -> dict:
        """Get aggregate stats. period: day|7d|30d|month|6mo|12mo|YYYY-MM-DD,YYYY-MM-DD"""
        metrics = metrics or ["visitors", "pageviews", "bounce_rate"]
        return self._get("/api/v1/stats/aggregate", {"period": period, "metrics": ",".join(metrics)})

    def timeseries(self, period: str = "30d", metrics: list[str] | None = None) -> dict:
        """Get daily breakdown for a period."""
        metrics = metrics or ["visitors"]
        return self._get("/api/v1/stats/timeseries", {"period": period, "metrics": ",".join(metrics)})

    def breakdown(self, property: str, period: str = "30d", metrics: list[str] | None = None) -> dict:
        """Get breakdown by property. Valid properties: event:page, visit:source, visit:device, visit:country"""
        metrics = metrics or ["visitors"]
        return self._get("/api/v1/stats/breakdown", {
            "period": period, "property": property, "metrics": ",".join(metrics)
        })

    def realtime_visitors(self) -> int:
        """Get current visitors (last 5 minutes)."""
        resp = requests.get(
            f"{self.base_url}/api/v1/stats/realtime/visitors",
            headers=self.headers,
            params={"site_id": self.site_id}
        )
        resp.raise_for_status()
        return int(resp.text)

    def _get(self, path: str, params: dict) -> dict:
        params["site_id"] = self.site_id
        resp = requests.get(f"{self.base_url}{path}", headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json()


# Usage example
if __name__ == "__main__":
    import os
    client = PlausibleClient(
        api_key=os.environ["PLAUSIBLE_API_KEY"],
        site_id=os.environ.get("PLAUSIBLE_SITE_ID", "yourdomain.com")
    )
    stats = client.aggregate(period="30d", metrics=["visitors", "pageviews"])
    print(f"Visitors: {stats['results']['visitors']['value']}")

    pages = client.breakdown(property="event:page", metrics=["visitors", "pageviews"])
    for page in pages["results"][:5]:
        print(f"{page['page']}: {page['visitors']} visitors")
