import os
import time
import requests
from urllib.parse import urlparse
from .connection import _post, EXPORT_URL, STATUS_URL, HEADERS

def export_contacts(properties, export_name="Contacts Export - API",objectType="CONTACT", fmt="XLSX"):
    
    if not properties:
        raise ValueError("❌ Debes proporcionar al menos una propiedad a exportar.")

    body = {
        "exportType": "VIEW", # Exportar vista sin lista predefinida :contentReference[oaicite:1]{index=1}
        "exportName": export_name,
        "format": fmt,  # CSV o XLSX
        "language": "EN",
        "objectType": objectType, # En mayúsculas según docs :contentReference[oaicite:2]{index=2}
        "objectProperties": properties,
        "publicCrmSearchRequest": {} # Obligatorio aunque vacío :contentReference[oaicite:3]{index=3}
    }

    j = _post(EXPORT_URL, body)
    export_id = j.get("id")
    print(f"🔄 Export job iniciado. ID = {export_id} - objectype = {objectType}")
    return export_id

def check_export_status(export_id):
    url = STATUS_URL.format(export_id)
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()

    status = data.get("status")
    file_url = None

    if status == "COMPLETE":
        result = data.get("result")
        if isinstance(result, str):
            # La URL está directamente en result
            file_url = result
        elif isinstance(result, dict):
            file_url = result.get("fileUrl")

    return status, file_url

def download_export(file_url, object_type="contacts"):
    resp = requests.get(file_url)
    resp.raise_for_status()
    
    parsed = urlparse(file_url)
    basename = os.path.basename(parsed.path)
    ext = os.path.splitext(basename)[1] or ".zip"
    timestamp = int(time.time())

    os.makedirs("data", exist_ok=True)
    filename = f"{object_type}_{timestamp}{ext}"
    filepath = os.path.join("data", filename)

    with open(filepath, "wb") as f:
        f.write(resp.content)

    print(f"✅ Archivo descargado: {filepath}")
    return filepath


