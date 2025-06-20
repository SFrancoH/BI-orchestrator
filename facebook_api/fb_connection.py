import os, requests
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'settings', '.env')
load_dotenv(dotenv_path=dotenv_path)

FB_MARKETING_TOKEN = os.getenv("FB_MARKETING_TOKEN")
raw_ids = os.getenv("FB_AD_ACCOUNT_IDS", "")
ad_account_ids = [id.strip() for id in raw_ids.split(",") if id.strip()]

BASE = "https://graph.facebook.com/v20.0"
HEADERS = { "Authorization": f"Bearer {FB_MARKETING_TOKEN}" }

def _get(endpoint, params=None):
    url = f"{BASE}{endpoint}"
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()

def test_marketing_api(ad_account_id):
    if not FB_MARKETING_TOKEN:
        print("❌ FB_MARKETING_TOKEN faltante.")
        return False
    try:
        res = _get(f"/act_{ad_account_id}", params={"fields": "account_id"})
        print("✅ Marketing token válido; Ad Account ID:", res.get("account_id"))
        return True
    except Exception as e:
        print("❌ Error Marketing API:", e)
        return False
