import logging
import argparse
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import *
from src.constants import *
from utils import common as cm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(filename, url, upload_to_mongo=False):
    html = cm.get_html(url)
    top_div = get_top_table_element(html)
    top_books_data = scrape_table_data(top_div)
    top_books_df = scraped_dict_to_csv(top_books_data, filename)
    if upload_to_mongo:
        insert_df_to_mongo(top_books_df)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog="goodreads_top100",
                    description="This program scrapes goodreads Top 100.")
    parser.add_argument("-o", "--output", required=False, default="./output/goodreads.csv")
    parser.add_argument("-u", "--url", required=False, default=GOODREADS_TOP_URL)
    parser.add_argument("-m", "--mongo", required=False, action='store_true')
    args = parser.parse_args()
    main(args.output, args.url, args.mongo)