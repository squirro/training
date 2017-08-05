# Examples for the Squirro Data Loader
Each folder is a separate example for how the Squirro Data Loader tool can be used to load data into squirro.
It is highly recommended to go through these in order, starting with the CSV example. Each example will build on the previous example and add a new feature.

## Getting the data loader
The Squirro Data Loader is distributed as part of the Squirro Toolbox. To install the Squirro Toolbox, follow the instructions [Here](https://github.com/squirro/training)

## Examples

* `csv` - An example of how to use the Squirro Data Loader to load a CSV file. If you are totally new to the data loader, this is probably the best place to start.
* `excel` - An example of how to use the Squirro Data Loader to load an Excel Spreadsheet
* `sql` - An example of how to use the Squirro Data Loader to load data from a SQL database
* `plugin` - An example of how to create custom plugins for the Squirro Data Loader to connect to any data source

## What does the Data Loader do?
Long story short, the data loader makes it easy to load data from any source into Squirro.
The dataloader will allow you to load data from CSV files, Excel Spreadsheets, and SQL databases out of the box, and can be extended throuh the use of Data Loader Plugins to be able to connect to any data source.
For more details on Data Loader plugins, see the README in the `plugin` folder here

### The Squirro item format
For data to be loaded, it has to be converted into the standard format used by all squirro items. The standard squirro item format is always a JSON object, and looks like this:
```json
{
  "body": "Squirro is...",
  "created_at": "2012-02-16T16:30:35",
  "title": "Squirro, Inc.",
  "id": "1",
  "link": "http://www.squirro.com",
  "keywords": {
    "Countries": [
      "United States",
      "Switzerland",
      "Germany",
      "United Kingdom",
      "Spain"
    ]
  },
  "abstract": "abstract text"
}
```
The standard squirro item format has a set of reserved fields (`title`, `body`, `id`, `link`, `created_at`, and `abstract`) which exist in the top level of the JSON object.

All other information that is included in a squirro item will be nested within an object within the top-level key `keywords`. Fields included here can have lists of values instead of only single values, and are referred to as facets. In the example shown above, the item has a single facet called "Countries", which has a total of 5 facet values
