import logging
import argparse
from src.utils import *
from src.constants import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(file):
    html = get_html(BBC_NEWS)
    article_links = list_article_links(html)
    data = []
    for link in article_links:
        logger.info(f"Scraping {link}")
        html = get_html(link)
        headline, author, body, tags = scrape_news(html)
        data.append(
            {
                "link": link,
                "headline": headline,
                "author": author,
                "body": body,
                "tags": tags
            }
        )
    export_json(data, file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog="bbc_news",
                    description="This program scrapes BBC News.")
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()
    main(args.output)