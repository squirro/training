# Using Pipelets with the Squriro Data Loader

This example shows how Pipelets can be used by the Data Loader to enrich data before it is uploaded to a Squirro server.

## What is a Pipelet?

Pipelets are plugins to the Squirro pipeline, used to customize how data is processed.
For more information on Pipelets, see the example [Here](https://github.com/squirro/training/tree/master/pipelets), or the Pipelet documentation [Here](https://squirro.atlassian.net/wiki/display/DOC/Pipelets)

### Pipelet configuration basics

To use a Pipelet with the Data Loader, the Data Load script must reference a Pipelet configutation file. This pipelet configuration file specifies which pipelets will be included, where the source code for each pipelet can be found, when the pipelets should be run, and any configuration required by the pipelet.

```json
{
    "CompanySizePipelet": {
        "file_location":"company_size.py",
        "stage":"before templating",
        "config": {}
    }
}
```

For more information on Pipelet configuration files for the Squirro Data Loader, see the documentation [Here](https://squirro.atlassian.net/wiki/display/DOC/Data+Loader+Pipelet+Config+Reference)

## Our Test Data Set
We will continue to use our test CSV data set from the previous examples.
The data set looks like this:

|id|company|ticker|ipo_date|number_employees|link|
|---|---|---|---|---|---|
|1|Apple|AAPL|1980-12-12T00:00:00|116000|https://finance.yahoo.com/quote/AAPL|
|2|Google|GOOG|2004-08-19T00:00:00|73992|https://finance.yahoo.com/quote/GOOG|
|3|Microsoft|MSFT|1986-03-13T00:00:00|120849|https://finance.yahoo.com/quote/MSFT|
|4|Amazon|AMZN|1997-05-15T00:00:00|341400|https://finance.yahoo.com/quote/AMZN|
|5|Intel|INTC|1978-01-13T00:00:00|106000|https://finance.yahoo.com/quote/INTC|

## Our Test Pipelet

Our test pipelet is the company size pipelet provided as an example Here.
This pipelet classifies each company as either a small, medium, large, or huge company based on it's number of employees.

## Constructing a Load Script
To use a pipelet with the Data Loader, reference a pipelet configuration file from your load script:

```bash
--pipelets-file 'pipelets.json' \
```
