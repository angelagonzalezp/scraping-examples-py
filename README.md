# scraping-examples-py

This repo contains some web scraping examples.

## Contents

1. [IMDb](#imdb)
    - [imdb_chart](#imdb_chart)
    - [moviemeter_cast](#moviemeter_cast)

## IMDb

### imdb_chart

[imdb_chart.py](IMDb\imdb_chart.py) scrapes IMDb most popular [movies](https://www.imdb.com/chart/moviemeter/) or [TV shows](https://www.imdb.com/chart/tvmeter/).

#### Parameters

* -o: output CSV file to store results.
* -t: optional flag. If specified, the script will scrape IMDb TV shows chart instead of moviemeter.

#### How to run the script
* Moviemeter: `cd .\IMDb\;python imdb_chart.py -o "./output/moviemeter-example.csv"`
* TVmeter: `cd .\IMDb\;python imdb_chart.py -o "./output/tvmeter-example.csv" -t`

> **NOTE:**  Powershell syntax.

### moviemeter_cast

[moviemeter_cast.py](IMDb\moviemeter_cast.py) scrapes the cast for the films in Moviemeter Chart.

#### Parameters

* -o: output JSON file to store results.
* -l: optional flag. It limits the number of actors and actresses retrieved for each film.

#### How to run the script
`cd .\IMDb\;python .\moviemeter_cast.py -l 3 -o .\output\moviemeter_cast.json`



