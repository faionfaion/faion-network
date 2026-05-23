# purpose: Stdlib calculator for RICE + WSJF + MoSCoW.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env python3
"""prio_method_and_wsjf.py — compute RICE / WSJF scores."""
from __future__ import annotations
import json, sys

def rice(reach, impact, confidence, effort):
    return (reach * impact * confidence) / max(effort, 0.1)

def wsjf(value, time_crit, risk_red, job_size):
    return (value + time_crit + risk_red) / max(job_size, 0.1)

if __name__ == '__main__':
    data = json.loads(sys.stdin.read())
    method = data.get('method', 'RICE')
    items = data['items']
    if method == 'RICE':
        for i in items: i['score'] = rice(i['reach'], i['impact'], i['confidence']/100.0, i['effort'])
    else:
        for i in items: i['score'] = wsjf(i['value'], i['time_crit'], i['risk_red'], i['job_size'])
    items.sort(key=lambda x: x['score'], reverse=True)
    print(json.dumps(items, indent=2))
