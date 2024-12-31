import logging
import argparse
from src.utils import *
from src.constants import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(file):
    html = get_html(BILLBOARD_HOT_100)
    songs = list_chart_items(html)
    songs.index.rename("position", inplace=True)
    songs.to_csv(file, sep=";")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog="billboard_hot100",
                    description="This program scrapes Billboard Hot 100 Chart.")
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()
    main(args.output)