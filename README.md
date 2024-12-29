# scraping-examples-py

This repo contains some web scraping examples.

## Contents

1. [IMDb](#imdb)

## IMDb

[imdb_chart.py](IMDb\imdb_chart.py) scrapes IMDb most popular [movies](https://www.imdb.com/chart/moviemeter/) or [TV shows](https://www.imdb.com/chart/tvmeter/).

### Parameters

* -o: output CSV file to store results.
* -t: optional flag. If specified, the script will scrape IMDb TV shows chart instead of moviemeter.

### How to run the script
* Moviemeter: `cd .\IMDb\;python imdb_chart.py -o "./output/moviemeter-example.csv"`
* TVmeter: `cd .\IMDb\;python imdb_chart.py -o "./output/tvmeter-example.csv" -t`

> **NOTE:**  Powershell syntax.

