# Using the Squirro Data Loader to Load a CSV File

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
|1|Apple|AAPL|1980-12-12T00:00:00|116000|https://finance.yahoo.com/quote/AAPL|
|2|Google|GOOG|2004-08-19T00:00:00|73992|https://finance.yahoo.com/quote/GOOG|
|3|Microsoft|MSFT|1986-03-13T00:00:00|120849|https://finance.yahoo.com/quote/MSFT|
|4|Amazon|AMZN|1997-05-15T00:00:00|341400|https://finance.yahoo.com/quote/AMZN|
|5|Intel|INTC|1978-01-13T00:00:00|106000|https://finance.yahoo.com/quote/INTC|

## Constructing a Load Script
Because the Squirro Data Loader takes lots of parameters as inputs, we will construct a load script which calls the dataloader with all of the required parameters included.

The example here is shown as a bash script, used on Linux or MacOS. For Windows, Batch scripts are used in place.

An example of a load script written in bash is included in `load.sh`.
We will go through this example load script line by line

```bash
#!/bin/bash
set -e
```

The very first line of this script tells us that it is a bash script, and instructs the computer on how to execute it.
The second line `set -e` tells bash that the execution of the script should stop if the script encounters an error. By default, bash scripts will continue running even after the script encounters an error.

```bash
CLUSTER="http://...squirro.net/"
TOKEN="...abc..."
PROJECT_ID="...123..."
```

Next, we add our cluster URL, user refresh token, and target project ID into environment variables which can be accessed by the script later.

```bash
squirro_data_load -v \
```

Once we Have all of the info that we need, the Data Loader is called. The extra option `-v` tells the Data Loader to run in verbose mode, so that we get more output that describes what the Data Loader is doing

```bash
    --cluster $CLUSTER \
    --token $TOKEN \
    --project-id $PROJECT_ID \
```

When we call the Data Loader, we pass in the values for cluster, token, and project_id that we defined above.

```bash
    --source-type csv \
    --source-file 'companies.csv' \
    --source-name 'CSV File' \
```

The source arguments tell the Data Loader what kind of data we are loading and where the original document can be found. Additionally, `--source-name` tells the Data Loader what the name of the source that shows up in the user interface for this data should be.

```bash
    --map-title 'ticker' \
    --map-body 'company' \
    --map-id 'id' \
    --map-url 'link' \
    --map-created-at 'ipo_date' \
```

Once the source data is defined, the next step is to map fields in the input data to the main fields within the Squirro items created. This tells the data loader which column should be used for the body, title, id, url, and created_at date for each item that the data loader sends to Squirro. The fields listed in single quotes on the right are the columns of the CSV file that are being used for each field of the Squirro item.

```bash
    --facets-file 'facets.json'
```
The last line of the load script tells the data loader where it can find the definition for the Facets to include in this data source. Facets are often used so that additional information (not used for the title, body, etc.) can be included within each item sent to Squirro. An example `facets.json` file is included here. In general, facet definitions have this form:
```hjson
{
    # The name of the column in the input data
    "ticker": {

        # The data type of the data stored in this facet (can also be int, float, or datetime)
        "data_type": "string",

        # The name of the facet that the values will be stored in
        "name": "ticker_symbol",

        # A display name to be used in the Squirro UI
        "display_name": "Ticker Symbol",

        # The name of a facet group that this facet is included in
        "group_name": "Companies",

        # Whether or not this facet is visible to an end user
        "visible": true,

        # Whether or not the values in this facet are indexed for full-text search
        "searchable": true,

        # Whether or not the values in this facet are available for typeahead completion
        "typeahead": true,

        # Whether or not the values in this facet are analyzed
        "analyzed": true,
    }
}
```
For more information on facet configuration, check the [Data Loader Facet Config Reference](https://squirro.atlassian.net/wiki/display/DOC/Data+Loader+Facet+Config+Reference)
### Using this Example
To use this example, you will only need to modify the values given to the environment variables on lines 4, 5, and 6. For details on how to find your cluster, token, or project_id, check the documentation page [Connecting to Squirro](https://squirro.atlassian.net/wiki/display/DOC/Connecting+to+Squirro)
