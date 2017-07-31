# Using the Squriro Data Loader to Load an Excel spreadsheet

## Setup
Before attempting this, it is assumed that the Squirro Data Loader has already been set up. For details on how to do the initial configuration, follow the instructions [here](#)
## Our Test Data Set
The Excel spreadsheet that we will load as a test is an excel version of the exact same data set used in the CSV example. The data set looks like this:

|id|company|ticker|ipo_date|number_employees|link|
|---|---|---|---|---|---|
|1|Apple|AAPL|1980-12-12T00:00:00|116000|https://finance.yahoo.com/quote/AAPL|
|2|Google|GOOG|2004-08-19T00:00:00|73992|https://finance.yahoo.com/quote/GOOG|
|3|Microsoft|MSFT|1986-03-13T00:00:00|120849|https://finance.yahoo.com/quote/MSFT|
|4|Amazon|AMZN|1997-05-15T00:00:00|341400|https://finance.yahoo.com/quote/AMZN|
|5|Intel|INTC|1978-01-13T00:00:00|106000|https://finance.yahoo.com/quote/INTC|

## Constructing a Load Script
Our load script for loading this excel sheet looks exactly the same as our CSV example, but with a different source specified. Specifically, we now have:
```bash
--source-type excel \
--source-file 'companies.xlsx' \
--source-name 'Excel Spreadsheet' \
```

These arguments tell the dataloader that we will now be loading an excel sheet, specify the location of the file, and the name of the source created for this data.
