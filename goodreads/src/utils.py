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

def get_top_table_element(html):
    try:
        table = html.find("div", attrs={"id": TOP_TABLE_DIV_ID})
    except Exception as error:
        raise error
    return table

def scrape_titles(top_table):
    titles_list = []
    books_href = []
    logging.info("scrape_titles(): get book titles and their URL.")
    try:
        titles_html = top_table.find_all("a", attrs={"class": BOOK_TITLE_CLASS})
        for title in titles_html: 
            href = title.get("href")
            books_href.append(href)
            title = title.find("span", attrs={"itemprop": "name"})
            titles_list.append(title.text)
        books_url = [BASE_URL + href for href in books_href]
    except Exception as error:
        raise error
    return titles_list, books_url

def scrape_authors(top_table):
    authors_list = []
    authors_href = []
    try:
        authors_html = top_table.find_all("a", attrs={"class": AUTHOR_NAME_CLASS})
        for author in authors_html: 
            href = author.get("href")
            authors_href.append(href)
            name = author.find("span", attrs={"itemprop": "name"})
            authors_list.append(name.text)
    except Exception as error:
        raise error
    return authors_list, authors_href

def format_rating(rating_string):
    """ rating_string: ' 4.57 avg rating — 29,297 ratings' """
    avg_mark = None
    votes = None
    try:
        splitted_rating = rating_string.split("—")
        avg_string = splitted_rating[0].replace("avg rating", "").strip()
        mark = re.findall("\d+\.\d+", avg_string)[0]
        rating_count = splitted_rating[1].replace("ratings", "").replace(",","").strip()
        avg_mark = float(mark)
        votes = int(rating_count)
    except Exception:
        logging.error(rating_string)
    return avg_mark, votes

def scrape_rating(top_table):
    avg_rating_list = []
    rating_count_list = []
    logging.info("scrape_rating(): get rating and votes for the book in the chart.")
    try:
        rating = top_table.find_all("span", attrs={"class": RATING_CLASS})
        for r in rating:
            avg, count = format_rating(r.text)
            avg_rating_list.append(avg)
            rating_count_list.append(count)
    except Exception as error:
        raise error
    return avg_rating_list, rating_count_list 

def scrape_table_data(table_html):
    try:
        titles, titles_href = scrape_titles(table_html)
        authors, authors_href = scrape_authors(table_html)
        avg_ratings, votes = scrape_rating(table_html)
        top_books_dictionary = {
            "title": titles,
            "book_url": titles_href,
            "author": authors,
            "author_url": authors_href,
            "rating": avg_ratings,
            "votes": votes
        }
    except Exception as error:
        raise error
    return top_books_dictionary

def scraped_dict_to_csv(data_dict, filename):
    df = pd.DataFrame.from_dict(data_dict)
    df.index = np.arange(1, len(df) + 1)
    df.index.rename("position", inplace=True)
    df.to_csv(filename, sep=";", encoding="utf-8")