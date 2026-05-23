"""Keyword dict format for add_keywords() function.

Match types: BROAD, PHRASE, EXACT
Bid is optional — omit to use ad group default CPC.
1,000,000 micros = $1.00
"""

keywords = [
    {
        "text": "project management software",
        "match_type": "PHRASE",
        # "bid_micros": 2000000  # $2.00 — optional keyword-level bid
    },
    {
        "text": "project management tool",
        "match_type": "EXACT",
    },
    {
        "text": "task management",
        "match_type": "BROAD",
        "bid_micros": 1500000,  # $1.50 — lower bid for broad match
    },
]
