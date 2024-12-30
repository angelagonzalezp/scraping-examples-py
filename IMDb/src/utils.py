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

def list_films(html):
    list = html.find_all("script", {"type" : "application/ld+json"})
    item_list = json.loads(list[0].get_text())["itemListElement"]
    return item_list

def list_cast(html):
    cast = []
    for element in html.find_all("a", class_= ACTOR_NAME_CLASS):
        actor = {}
        actor["name"] = element.get_text()
        actor["imdb_url"] = BASE_URL + element.get("href")
        cast.append(actor)
    return cast

def get_actor_birthdate(html):
    born_element = html.find_all("span", class_=DATE_OF_BIRTH)
    birthdate = None
    try:
        birthdate = born_element[1].get_text()
    except Exception as err:
        logger.error(err)
    return birthdate

def get_actor_filmography(html):
    filmography = []
    try:
        items = html.find_all("a", class_=ACTOR_PREVIOUS_FILMOGRAPHY)
        for item in items:
            film = {}
            film["name"] = item.get_text()
            film["url"] = BASE_URL + item.get("href")
            filmography.append(film)
    except Exception as e:
        logger.error(e)
    return filmography

def get_actor_info(html, actor):
    actor["birthdate"] = get_actor_birthdate(html)
    actor["filmography"] = get_actor_filmography(html)
    return actor