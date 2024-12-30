#%%
import logging
import json
import time
import numpy as np
from operator import itemgetter
from imdb_chart import *
from src.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(file=None, limit=None):
    html = get_html(URL_MOVIEMETER)
    chart = list_films(html)
    actors_and_actresses = []
    for title in chart[0:TOP_LIMIT]:
        item_info = extract_item_info(title)
        title_url = item_info["url"]
        html = get_html(title_url)
        logger.info(f"Get cast for film {item_info['name']}")
        actors = list_cast(html)
        if limit:
            actors = actors[0:limit]
        for actor in actors:
            time.sleep(np.random.randint(1,10))
            try:
                already_scraped = list(map(itemgetter("name"), actors_and_actresses))
            except Exception as error:
                logger.error(error)
            if(actor["name"] not in already_scraped):
                logger.info(f"Scrape info from {actor['name']} IMDb web")
                html_actor = get_html(actor["imdb_url"])
                actor = get_actor_info(html_actor, actor)
                actors_and_actresses.append(actor)
            else:
                logger.info(f"{actor['name']} info is already retrieved.")
    if(file):
        with open(file, "w", encoding='utf-8') as f:
            json.dump(actors_and_actresses, f)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog="",
                    description="""This program scrapes the cast of the films in Moviemeter chart. 
                        The number of actors fetched can be limited with --limit parameter.""")
    parser.add_argument("-o", "--output", required=False)
    parser.add_argument("-l", "--limit", required=False, type=int)
    args = parser.parse_args()
    main(args.output, args.limit)
# %%
