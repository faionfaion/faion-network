# bottom_up_tam.py — calculate bottom-up TAM/SAM/SOM with 3-year projection
# Inputs: ICP company count, adoption rate, ACV, annual growth rate
# Output: dict with buyers, TAM year 1, TAM year 3

def calc_market(
    icp_companies: int,
    adoption_rate: float,       # 0.0-1.0; fraction of ICP reachable
    acv_usd: float,             # average annual contract value in USD
    growth_rate_yoy: float,     # 0.0-1.0; e.g. 0.25 = 25% YoY growth
    sam_fraction: float = 1.0,  # fraction of TAM that is addressable (SAM)
    som_fraction: float = 0.05, # realistic 3-5 year market share (SOM)
) -> dict:
    buyers = icp_companies * adoption_rate
    tam = buyers * acv_usd
    sam = tam * sam_fraction
    som = sam * som_fraction
    tam_y3 = tam * ((1 + growth_rate_yoy) ** 3)
    return {
        "buyers": int(buyers),
        "tam_year1_usd": round(tam),
        "sam_year1_usd": round(sam),
        "som_year1_usd": round(som),
        "tam_year3_usd": round(tam_y3),
        "assumptions": {
            "icp_companies": icp_companies,
            "adoption_rate": adoption_rate,
            "acv_usd": acv_usd,
            "growth_rate_yoy": growth_rate_yoy,
            "sam_fraction": sam_fraction,
            "som_fraction": som_fraction,
        },
    }


# Example — add source citations before using in any external doc
result = calc_market(
    icp_companies=500_000,   # source: estimate, unvalidated
    adoption_rate=0.05,      # source: estimate, unvalidated
    acv_usd=10_000,          # source: internal pricing model
    growth_rate_yoy=0.25,    # source: Gartner 2025 report
)
print(result)
# {'buyers': 25000, 'tam_year1_usd': 250000000, 'sam_year1_usd': 250000000,
#  'som_year1_usd': 12500000, 'tam_year3_usd': 488281250, 'assumptions': {...}}
