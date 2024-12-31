import requests
import re
from bs4 import BeautifulSoup
import logging
import pandas as pd
import numpy as np
from .constants import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_html(url):
    response = requests.get(url, headers=HEADERS)
    try: 
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)
    html = BeautifulSoup(response.text, "html.parser")
    return html

def list_chart_items(html):
    partial_class = "^" + CHART_LI + ".*"
    li_elements = html.find_all("li", attrs={"class": re.compile(partial_class)})
    songs = []; authors = []
    for li in li_elements:
        try:
            title = li.findChildren("h3" , recursive=False,attrs={"id": re.compile(TITLE_ID)})
            if(len(title)>0):
                author_span = li.findChildren("span", recursive=False, attrs={"class": re.compile(AUTHOR_SPAN)})
                songs.append(title[0].get_text().strip())
                authors.append(author_span[0].get_text().strip())
        except IndexError:
            pass
        except Exception as err:
            logger.error(err)
    return pd.DataFrame({"song": songs, "author": authors}, index=np.arange(1,101))