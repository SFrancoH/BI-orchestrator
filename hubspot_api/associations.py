import pandas as pd
from .connection import _post, BASE_URL

def fetch_deal_contact_associations(deal_ids):
    if not deal_ids:
        return pd.DataFrame(columns=["deal_id", "contact_id"])
    url = f"{BASE_URL}/crm/v4/associations/deal/contact/batch/read"
    payload = {"inputs": [{"id": str(d)} for d in deal_ids]}
    r = _post(url, payload)
    rows = []
    for item in r.get("results", []):
        deal = item.get("from", {}).get("id")
        tos = item.get("to", [])
        for t in tos:
            rows.append({"deal_id": deal, "contact_id": t.get("id")})
    print(f"✅ Obtenidas {len(rows)} asociaciones Deal→Contact.")
    return pd.DataFrame(rows)
