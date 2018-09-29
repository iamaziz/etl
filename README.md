

## What

This repo contains script for demonstrating a simple ETL data pipeline. Starting from extracting data from the source, transforming into a desired format, and loading into a SQLite file.

Then, perform simple analysis queries on the stored data. See: [analysis notebook](analysis.ipynb).

> Note: The used data is about the US population and unemployment rate over the past decade.


<hr>

## Getting started

First, install the dependencies
```
$ pip install -r requirements.txt
```
> Note: preferable, run under a virtualenv 
> 
> ```
> $ virtualenv .env -p python3
> $ source .env/bin/activate
> $ pip install -r requirements.txt
> ```

Second, run the main pipeline file

```
$ python pipeline.py
Data Pipeline created
	 extracting data from source ....
	 formatting and transforming data ...
	 loading into database ...

Done. See: result in "db.sqlite"
```

<hr>

## Requirements

- pandas
- xlrd (for reading excel file)
- Python >= 3.6


<hr>

## Data source and description



POPULATION BY METROPOLITAN AREA AND COUNTY


- cbsa-est2017-alldata.csv
	- data source:
		https://www.census.gov/data/tables/2017/demo/popest/total-metro-and-micro-statistical-areas.html#par_textimage
	- download link:
		https://www2.census.gov/programs-surveys/popest/datasets/2010-2017/metro/totals/cbsa-est2017-alldata.csv
	- dataset description:
		https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2017/cbsa-est2017-alldata.pdf



UNEMPLOYMENT BY COUNTY 


- Unemployment.xls
	- data source:
		https://catalog.data.gov/dataset/county-level-data-sets
		https://www.ers.usda.gov/data-products/county-level-data-sets/download-data
	- download link:
		https://www.ers.usda.gov/webdocs/DataFiles/48747/Unemployment.xls
	- description:
		see the sheet "Variable Descriptions" in the same `xls` file
