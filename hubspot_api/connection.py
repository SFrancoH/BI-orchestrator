import os
import requests
import json
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', 'settings', '.env')
load_dotenv(dotenv_path=env_path)

# Obtén la variable tanto si está definida como cadena
props_contacts = os.getenv("HUBSPOT_PROPS_CONTACTS", "[]")
props_deals = os.getenv("HUBSPOT_PROPS_DEALS", "[]")
HUBSPOT_TOKEN = os.getenv("HUBSPOT_API_KEY")

BASE_URL = "https://api.hubapi.com"

# Endpoints correctos para exportación
EXPORT_URL = f"{BASE_URL}/crm/v3/exports/export/async"
STATUS_URL = f"{BASE_URL}/crm/v3/exports/export/async/tasks/{{}}/status"
ACCOUNT_URL = f"{BASE_URL}/account-info/v3/details"

# Carga variables de entorno

try:
    HUBSPOT_PROPS_CONTACTS = json.loads(props_contacts)
    HUBSPOT_PROPS_DEALS = json.loads(props_deals)

    if not isinstance(HUBSPOT_PROPS_CONTACTS, list) or \
       not isinstance(HUBSPOT_PROPS_DEALS, list):
        raise ValueError("❌ HUBSPOT_PROPS debe ser una lista JSON válida")

except (json.JSONDecodeError, ValueError) as err:
    print(f"⚠️ Error cargando props: {err}")
    HUBSPOT_PROPS_CONTACTS = []
    HUBSPOT_PROPS_DEALS = []


HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type": "application/json"
}

def _get(url):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def _post(url, payload):
    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()

def test_connection():
    """
    Verifica que el token funcione usando un endpoint.
    Retorna True si se conecta correctamente, False si falla.
    """
    try:
        j = _get(ACCOUNT_URL)
        portal_id = j.get("portalId", "<desconocido>")
        print("✅ Conexión exitosa. Portal ID:", portal_id)
        return True

    except Exception as e:
        print("❌ Error al conectar a HubSpot:", e)
        return False
