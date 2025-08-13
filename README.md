# scraping-examples-py

This repo contains some web scraping examples.

## Contents

1. [IMDb](#imdb)
    - [imdb_chart](#imdb_chart)
    - [moviemeter_cast](#moviemeter_cast)
2. [Billboard](#billboard)
    - [billboard_hot100](#billboard_hot100)
3. [goodreads](#goodreads)
    - [goodreads_top100](#goodreads_top100)
4. [BBC](#BBC)
    - [bbc_news](#bbc_news)
5. [CoinMarketCap](#CoinMarketCap)
    - [trending-cryptocurrencies](#trending-cryptocurrencies)

## IMDb

### imdb_chart

[imdb_chart.py](https://github.com/angelagonzalezp/scraping-examples-py/blob/main/IMDb/imdb_chart.py) scrapes IMDb most popular [movies](https://www.imdb.com/chart/moviemeter/) or [TV shows](https://www.imdb.com/chart/tvmeter/).

#### Parameters

* -o: output CSV file to store results.
* -t: optional flag. If specified, the script will scrape IMDb TV shows chart instead of moviemeter.

#### How to run the script
* Moviemeter: `cd .\IMDb\;python imdb_chart.py -o "./output/moviemeter-example.csv"`
* TVmeter: `cd .\IMDb\;python imdb_chart.py -o "./output/tvmeter-example.csv" -t`

> **NOTE:**  Powershell syntax.

### moviemeter_cast

[moviemeter_cast.py](https://github.com/angelagonzalezp/scraping-examples-py/blob/main/IMDb/moviemeter_cast.py) scrapes the cast for the films in Moviemeter Chart.

#### Parameters

* -o: output JSON file to store results.
* -l: optional flag. It limits the number of actors and actresses retrieved for each film.

#### How to run the script
`cd .\IMDb\;python .\moviemeter_cast.py -l 3 -o .\output\moviemeter_cast.json`

## Billboard

### billboard_hot100

[billboard_hot100.py](https://github.com/angelagonzalezp/scraping-examples-py/blob/main/Billboard/billboard_hot100.py) scrapes Billboard [Hot 100](https://www.billboard.com/charts/hot-100/) chart. So far, this script fetches the name of the song and author.

#### Parameters

* -o: output CSV file to store results.

#### How to run the script
`cd .\Billboard\;python .\billboard_hot100.py -o .\output\billboard_top100.csv`

## goodreads

### goodreads_top100
[goodreads_top100.py](https://github.com/angelagonzalezp/scraping-examples-py/blob/main/goodreads/goodreads_top100.py) scrapes Goodreads Top 100 - Highest Rated Books on Goodreads with at least 10,000 Ratings

#### Parameters

* -o: output CSV file to store results.
* -m: optional flag. If specified, it writes the scraped data to a MongoDB collection specified as environment variables.

#### How to run the script
`cd .\goodreads\;python .\goodreads_top100.py -o .\output\goodreads_top100.csv [-m]`

## BBC

### bbc_news
[bbc_news.py](https://github.com/angelagonzalezp/scraping-examples-py/blob/main/BBC/bbc_news.py) scrapes BBC News iterating through articles.

#### Parameters

* -o: output JSON file to store results.

#### How to run the script
`cd .\BBC\;python .\bbc_news.py -o .\output\bbc-news-example.json`

## CoinMarketCap

### trending-cryptocurrencies
[trending-cryptocurrencies.py](https://github.com/angelagonzalezp/scraping-examples-py/blob/main/coinmarketcap/trending-cryptocurrencies.py) scrapes the hottest trending cryptocurrencies on CoinMarketCap.

#### Parameters

* -o: output CSV file to store results.

#### How to run the script
`cd .\coinmarketcap\;python .\trending-cryptocurrencies.py -o .\output\trending-cryptocurrencies.csv`