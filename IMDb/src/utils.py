import requests
import json
from bs4 import BeautifulSoup
from .constants import *

def get_html(url):
    response = requests.get(url, headers=HEADERS)
    try: 
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)
    html = BeautifulSoup(response.text, "html.parser")
    return html

def list_films(html):
    list = html.find_all("script", {"type" : "application/ld+json"})
    item_list = json.loads(list[0].get_text())["itemListElement"]
    return item_list