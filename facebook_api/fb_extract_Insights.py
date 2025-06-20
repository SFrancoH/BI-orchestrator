import os
import json
import locale
import pandas as pd
from datetime import datetime, timedelta
from facebook_api.fb_connection import _get
from facebook_api.adsets_utils import get_data_adsets
from requests.exceptions import HTTPError


def daterange(start_date, end_date, step_days=30):
    current = start_date
    while current <= end_date:
        next_date = min(current + timedelta(days=step_days - 1), end_date)
        yield current, next_date
        current = next_date + timedelta(days=1)


def extract_ad_id_data(ad_account_id, date_start, date_stop):
    fields = 'spend,reach,frequency,ad_id,ad_name,impressions,actions'
    date_range = {"since": date_start, "until": date_stop}
    ret = []

    try:
        adsets = json.loads(get_data_adsets(ad_account_id))
    except HTTPError as e:
        print(f"❌ Error al obtener adsets para {ad_account_id}: {e}")
        return []

    for page in adsets:
        resp = _get(
            f"/{page['adset_id']}/insights",
            params={
                "level": "ad",
                "fields": fields,
                "time_range": json.dumps(date_range),
                "time_increment": 1
            }
        )
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        for insight in resp.get("data", []):
            record = insight.copy()
            actions = insight.get("actions", [])
            convo = next(
                (int(a["value"]) for a in actions
                 if a["action_type"] == 'onsite_conversion.messaging_conversation_started_7d'),
                0
            )
            record["results"] = convo
            record["cost_per_result"] = float(insight.get("spend", 0)) / convo if convo else 0.0
            record["adset_budget"] = page.get("daily_budget")
            record["page"] = page.get("page") if "page" in page else None
            ret.append(record)

    return ret


def batch_download_insights(ad_account_id, start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    all_data = pd.DataFrame()

    for since_dt, until_dt in daterange(start, end):
        since_str = since_dt.strftime("%Y-%m-%d")
        until_str = until_dt.strftime("%Y-%m-%d")
        print(f"📥 Descargando métricas desde {since_str} hasta {until_str}...")

        new_data = pd.DataFrame(extract_ad_id_data(ad_account_id, since_str, until_str))

        if not new_data.empty:
            all_data = pd.concat([all_data, new_data], ignore_index=True)
            all_data.drop_duplicates(subset=["date_start", "ad_id"], inplace=True)

    return all_data
