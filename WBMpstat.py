import io
import csv
import requests as r
import json
from base64 import b64decode

def get_tags_search(text):
    try:
        headers = {
            'Cookie': 'sv_auth='
        }
        jsoon = {
            "startRow": 0,
            "endRow": 20,
            "filterModel": {"word": {"filterType": "text", "type": "contains", "filter": f"{text}"}},
            "sortModel": [{"sort": "desc", "colId": "wb_count"}]
        }
        rg = r.post(f'https://analitika-wb-ozon.pro/api/seo/keywords/selection?', headers=headers, json=jsoon)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
