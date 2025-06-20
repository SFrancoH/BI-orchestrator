import os
from facebook_api.fb_connection import _get

def list_adsets(ad_account_id):
    """
    Lista AdSets de tu cuenta usando Marketing API.
    """
    resp = _get(f"/act_{ad_account_id}/adsets", params={"fields": "id,daily_budget,page"})
    return [
        {"adset_id": a["id"], "daily_budget": a.get("daily_budget"), "page": a.get("page")}
        for a in resp.get("data", [])
    ]
