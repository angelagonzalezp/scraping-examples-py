import logging
import argparse
import pandas as pd
from src.utils import *
from src.constants import *

def create_basic_info_dict(web_item, properties_list):
    film_info_dict = {}
    for prop in properties_list:
        try:
            film_info_dict[prop] = web_item[prop]
        except Exception as error:
            logging.error("create_basic_info_dict(): " + error)
    return film_info_dict

def add_rating_info(web_item, film_dict, rating_fields):
    for field in rating_fields:
        film_dict[field] = None
        try:
            film_dict[field] = web_item["aggregateRating"][field]
        except KeyError:
            logging.error(f"add_rating_info(): No aggregateRating.{field} value for film {film_dict['name']}")
    return film_dict

def extract_item_info(film):
    film_info = film["item"]
    film_info_dict = create_basic_info_dict(film_info, FILM_PROPERTIES)
    film_info_dict = add_rating_info(film_info, film_info_dict, AGGREGATE_RATING)
    return film_info_dict

def main(output_file, tv=False):
    url = URL_MOVIEMETER
    if(tv):
        url = URL_TVMETER
    html = get_html(url)
    titles = list_films(html)
    records = []
    for title in titles:
        item_info = extract_item_info(title)
        records.append(item_info)
    df = pd.DataFrame.from_dict(records)
    df.index += 1 
    df.to_csv(output_file, index_label="position")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog="idmb-popular-movies",
                    description="This program scrapes IMDB charts moviemeter/tvmeter")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-t", "--tvmeter", action='store_true')
    args = parser.parse_args()
    main(args.output, args.tvmeter)

