import requests
import json
from bs4 import BeautifulSoup
import logging
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

def list_article_links(html):
    try:
        main_element = html.find("main", id=MAIN_CONTENT_ID)
        links = [
            BASE_URL + a["href"] for a in main_element.find_all("a", href=True)
            if a["href"].startswith(ARTICLES_HREF)
        ]  
        logger.info(f"{len(links)} links found.")
    except Exception as e:
        raise SystemExit(e)
    return links 

def scrape_headline(html):
    try:
        headline_div = html.find("div", attrs=HEADLINE_ATTRS)
        headline = headline_div.find("h1").get_text(strip=True)
    except Exception as e:
        raise SystemExit(e)
    return headline

def scrape_author(html):
    try:
        byline_div = html.find("div", attrs=BYLINE_ATTRS)
        author = byline_div.find("span").get_text(strip=True)
    except Exception as e:
        raise SystemExit(e)
    return author

def scrape_tags(html):
    try:
        tags_div = html.find("div", attrs=TAGS_ATTRS)
        tags_a = tags_div.find_all("a")
        tags = [tag.get_text(strip=True) for tag in tags_a]
    except Exception as e:
        raise SystemExit(e)
    return tags

def scrape_body(html):
    try:
        body_div = html.find_all("div", attrs=BODY_DIV_ATTRS)
        body_p = []
        for div in body_div:
            body_p.extend(div.find_all("p"))
        paragraphs = [p.get_text(strip=True) for p in body_p]
        body = "\n".join(paragraphs)
    except Exception as e:
        raise SystemExit(e)
    return body

def scrape_news(html):
    headline = scrape_headline(html)
    author = scrape_author(html)
    body = scrape_body(html)
    tags = scrape_tags(html)
    return headline, author, body, tags

def export_json(data, filename):
    json_output = json.dumps(data)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json_output)
    