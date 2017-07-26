# Using the Squriro Data Loader to Load a CSV File

## Testing the Data Loader
Before we start, let's test that the Squirro Data Loader is installed and ready to use. To check for this, try to run the Data Loader and just show the help. This will let us make sure that the Data Loader is installed and set up correctly.

```bash
$ squirro_data_load --help
usage: squirro_data_load [-h] [--version] [--verbose] [--log-file LOG_FILE]
                         [--parallel-uploaders PARALLEL_UPLOADERS]
                         [--meta-db-dir META_DB_DIR]
                         [--meta-db-file META_DB_FILE] [--map-title MAP_TITLE]
                         [--map-abstract MAP_ABSTRACT]
                         [--map-created-at MAP_CREATED_AT] [--map-id MAP_ID]
                         [--map-body [MAP_BODY [MAP_BODY ...]]]
...
```
If you get the output shown above, the Data Loader is installed and ready to use.

## Our Test Data Set
The CSV file that we will load as a test has a list of companies with some basic data about each of them. The data set looks like this:

|id|company|ticker|ipo_date|number_employees|link|
|---|---|---|---|---|---|
|1|Apple|AAPL|<span style="font-size: 10px;">1980-12-12T00:00:00</span>|116000|https://finance.yahoo.com/quote/AAPL|
|2|Google|GOOG|2004-08-19T00:00:00|73992|https://finance.yahoo.com/quote/GOOG|
|3|Microsoft|MSFT|1986-03-13T00:00:00|120849|https://finance.yahoo.com/quote/MSFT|
|4|Amazon|AMZN|1997-05-15T00:00:00|341400|https://finance.yahoo.com/quote/AMZN|
|5|Intel|INTC|1978-01-13T00:00:00|106000|https://finance.yahoo.com/quote/INTC|
