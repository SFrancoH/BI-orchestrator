import time
import uuid
import pandas as pd
from hubspot_api.connection import test_connection, HUBSPOT_PROPS_CONTACTS, HUBSPOT_PROPS_DEALS
from hubspot_api.export_contacts import export_contacts, check_export_status, download_export
from requests.exceptions import HTTPError
from file_utils.xlsx_utils import read_xlsx, get_first_column_ids
from utils.io_utils import rename_xlsx, delete_all_xlsx

def download_contacts():
    try:
        eid = export_contacts(properties=HUBSPOT_PROPS_CONTACTS)
        file_url = None
    except HTTPError as e:
        if e.response.status_code == 409:
            print("🔁 Job duplicado detectado. Esperando para reintentar...")
            time.sleep(80)
            eid = export_contacts(properties=HUBSPOT_PROPS_CONTACTS)
            file_url = None
        else:
            raise

    print("✅ Job iniciado con ID:", eid)

    while True:
        status, file_url = check_export_status(eid)
        print("Estado del export:", status)
        if status == "COMPLETE":
            break
        if status == "FAILED":
            raise Exception("❌ La exportación falló.")
        time.sleep(300)

    # 5. Descargar el ZIP
    print("✅ Export COMPLETE. Descargando archivo...")
    zip_path = download_export(file_url)
    rename_xlsx(zip_path,"contacs.xlsx")

def download_deals():
    try:
        eid = export_contacts(properties=HUBSPOT_PROPS_DEALS, export_name="Deals Export - API", objectType="DEAL")
        file_url = None
    except HTTPError as e:
        if e.response.status_code == 409:
            print("🔁 Job duplicado detectado. Esperando para reintentar...")
            time.sleep(80)
            eid = export_contacts(properties=HUBSPOT_PROPS_DEALS, export_name="Deals Export - API", objectType="DEAL")
            file_url = None
        else:
            raise

    print("✅ Job iniciado con ID:", eid)

    while True:
        status, file_url = check_export_status(eid)
        print("Estado del export:", status)
        if status == "COMPLETE":
            break
        if status == "FAILED":
            raise Exception("❌ La exportación falló.")
        time.sleep(300)

    # 5. Descargar el ZIP
    print("✅ Export COMPLETE. Descargando archivo...")
    zip_path = download_export(file_url,object_type="deals")
    
    deals_df = read_xlsx(zip_path)
    deals_ids = get_first_column_ids(zip_path)
    assoc_df =  fetch_deal_contact_associations(deal_ids)
    
    rename_xlsx(zip_path,"deals.xlsx")



if __name__ == "__main__":
    if test_connection():
        delete_all_xlsx()
        download_contacts()
        time.sleep(60)
        download_deals()

    else:
        print('Error en la coneccion') 