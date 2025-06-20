import time
import uuid
import pandas as pd

from datetime import date, timedelta
import calendar

from requests.exceptions import HTTPError

from hubspot_api.connection import test_connection, HUBSPOT_PROPS_CONTACTS, HUBSPOT_PROPS_DEALS
from hubspot_api.export_contacts import export_contacts, check_export_status, download_export

from facebook_api.fb_connection import test_marketing_api,ad_account_ids
from facebook_api.fb_extract_Insights import batch_download_insights

from file_utils.xlsx_utils import read_xlsx, get_first_column_ids, save_xlsx_incremental
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
    rename_xlsx(zip_path,"deals.xlsx")

def calcular_rango_consulta():
    hoy = date.today()
    
    if hoy.day == 1:
        # Estamos el día 1 → consultamos el mes anterior completo
        mes_anterior = hoy.month - 1 or 12
        anio = hoy.year if hoy.month > 1 else hoy.year - 1

        dia_inicio = date(anio, mes_anterior, 1)
        dia_final = date(anio, mes_anterior, calendar.monthrange(anio, mes_anterior)[1])
    else:
        # Estamos en cualquier otro día → consultamos del 1 hasta ayer del mes actual
        dia_inicio = hoy.replace(day=1)
        dia_final = hoy - timedelta(days=1)
    
    return dia_inicio, dia_final

def extract_facebook_ads(ad_account_id):
    start_date, end_date = calcular_rango_consulta()
    df = batch_download_insights(ad_account_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    save_xlsx_incremental(df, "XmartFi.xlsx")

if __name__ == "__main__":
    if test_connection() and test_marketing_api(ad_account_ids[0]):
        #delete_all_xlsx()
        #download_contacts()
        #time.sleep(60)
        #download_deals()
        extract_facebook_ads(ad_account_ids[0])
        
    else:
        print('Error en la coneccion') 