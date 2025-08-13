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
    logger.info(f"Accessing {url}...")
    response = requests.get(url, headers=HEADERS)
    try: 
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)
    html = BeautifulSoup(response.text, "html.parser")
    return html

def normalize_values(values):
    return [x.replace("$", "").replace(",", "") for x in values]

def scrape_table(html):
    # HEADERS
    head = html.find("thead") 
    if head:
        logger.info("Scraping table headers...")
        p_elements = head.find_all("p")
        table_headers = []
        for p in p_elements[1:-1]:
            # skip '#' column
            table_headers.append(p.text)
            
        # BODY
        body = html.find("tbody")
        if body:
            logger.info("Scraping body content...")
            rows = body.find_all("tr")
            df_rows = []
            for row in rows:
                row_data = []
                cells = row.find_all("td")
                for cell in cells[2:-1]:
                    row_data.append(cell.text)
                row_data[1:] = normalize_values(row_data[1:])
                df_rows.append(row_data)
            df = pd.DataFrame(df_rows, columns=table_headers, index=range(1, len(df_rows) + 1))
            df['Name'], df['Initials'] = zip(*df.apply(lambda row: row['Name'].split(str(row.name)), axis=1))
            df.index.name = 'Position'
            return df
        else:
            logger.warning("Table body was not found")
    else:
        logger.warning("thead element was not found")