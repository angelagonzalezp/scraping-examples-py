import re
import logging
import os
import random
import sys
import pandas as pd
import numpy as np
from src.constants import *
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from time import sleep
from random import randint
from utils import common as cm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def format_string_date(date_str):
    # July 3, 2018
    try:
        formatted_date = datetime.strptime(date_str, "%B %d, %Y")
        return formatted_date
    except ValueError:
        logger.error(f"Cannot convert {date_str} to the desired format")

def scrape_book_details(book_href, proxy=None):
    logger.info(f"Scraping book details: {book_href}")
    html = cm.get_html(book_href, proxy=proxy)
    if html:
        details = {}
        try:
            reviews_count = html.find("span", attrs=REVIEWS_COUNT_ATTR)
            description = html.find("div", attrs=DESCRIPTION_ATTR)
            first_published = html.find("p", attrs=FIRST_PUBLISHED_ATTR)
            details = {
                "reviews_count": int(reviews_count.text.replace("reviews", "").replace(",","").strip()),
                "description": description.text,
                "first_published": format_string_date(first_published.text.replace("First published", "").replace("Published", "").strip())
            }
        except Exception as e:
            logger.error(e)
        return details

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
            "votes": votes,
            "reviews": [],
            "description": [],
            "first_published": []
        }
        
        #proxies = cm.get_free_proxies()
        for url in top_books_dictionary["book_url"]:
            sleep(randint(1,20))
            #details = scrape_book_details(url, proxy=random.choice(proxies))
            details = scrape_book_details(url)
            try:
                top_books_dictionary["reviews"].append(details["reviews_count"])
                top_books_dictionary["description"].append(details["description"])
                top_books_dictionary["first_published"].append(details["first_published"])
            except TypeError:
                logger.warning(f"Failed to retrieve book details for url {url}")
            
    except Exception as error:
        raise error
    return top_books_dictionary

def scraped_dict_to_csv(data_dict, filename):
    df = pd.DataFrame.from_dict(data_dict)
    df.index = np.arange(1, len(df) + 1)
    df.index.rename("position", inplace=True)
    df.to_csv(filename, sep=";", encoding="utf-8")
    return df

def connect_to_mongo(mongo_uri, database):
    try:
        logging.info("connect_to_mongo(): Connecting to MongoDB")
        client = MongoClient(mongo_uri) 
        db = client[database]
    except Exception as mongo_error:
        raise mongo_error
    return db
    
def get_mongo_collection(db_object, colname):
    try:
        collection = db_object[colname]
    except Exception as err:
        raise err
    return collection

def insert_df_to_mongo(df):
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")
    MONGO_COLLECTION = os.getenv("MONGO_COL")
    db = connect_to_mongo(MONGO_URI, MONGO_DB)
    collection = get_mongo_collection(db, MONGO_COLLECTION)
    try:
        logging.info(f"insert_df_to_mongo(): Insert documents to {MONGO_COLLECTION}")
        collection.insert_many(df.to_dict('records'))
    except Exception as insert_error:
        raise insert_error
        