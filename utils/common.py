import requests
import random
from bs4 import BeautifulSoup
from .constants import *

def get_free_proxies():
    response = requests.get(FREE_PROXIES_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("div", attrs= PROXIES_TABLE_ATTR)
    rows = table.tbody.find_all('tr')
    proxies = []
    for row in rows:
        cols = row.find_all('td')
        ip = cols[0].text
        port = cols[1].text
        https = cols[6].text == 'yes'
        if https:
            proxies.append(f"http://{ip}:{port}")
    return proxies

def get_html(url, proxy=None):
    if proxy:
        response = requests.get(url, headers=HEADERS, proxies={"http": proxy, "https": proxy}, timeout=10)
    else:
        headers = HEADERS = {
            'User-Agent': random.choice(USER_AGENTS_LIST),
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
        }
        response = requests.get(url, headers=headers, timeout=10)
    try: 
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)
    html = BeautifulSoup(response.text, "html.parser")
    return html