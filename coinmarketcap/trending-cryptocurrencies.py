import logging
import argparse
from src.utils import *
from src.constants import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(file):
    html = get_html(TRENDING_CRYPTO_URL)
    table = scrape_table(html)
    table.to_csv(file, sep=",")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog="trending-criptocurrencies",
                    description="This program scrapes Trending Cryptocurrencies On CoinMarketCap.")
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()
    main(args.output)