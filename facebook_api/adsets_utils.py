import json
from .fb_utils import list_adsets

def get_data_adsets(ad_account_id):
    adsets = list_adsets(ad_account_id)
    return json.dumps(adsets)
