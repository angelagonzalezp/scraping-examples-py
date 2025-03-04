import logging
import argparse
from src.utils import *
from src.constants import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(filename, upload_to_mongo=False):
    html = get_html(GOODREADS_TOP_URL)
    top_div = get_top_table_element(html)
    top_books_data = scrape_table_data(top_div)
    top_books_df = scraped_dict_to_csv(top_books_data, filename)
    if upload_to_mongo:
        insert_df_to_mongo(top_books_df)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog="goodreads_top100",
                    description="This program scrapes goodreads Top 100.")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-m", "--mongo", required=False, action='store_true')
    args = parser.parse_args()
    main(args.output, args.mongo)