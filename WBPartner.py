import io
import csv
import requests as r
import json
from base64 import b64decode

def get_tags_by_search(message, WBToken, x_supplier_id):
    query = message.text
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://trending-searches.wb.ru/api?itemsPerPage=19&offset=0&period=week&query={query}&sort=desc', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn