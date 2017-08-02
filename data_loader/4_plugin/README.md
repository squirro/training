# Custom Plugins for the Squriro Data Loader

This example shows how custom plugins can be created for the Squirro Data Loader. While the Data Loader supports connections to csv files, excel sheets, and SQL databases out of the box, these plugins allow the data loader to connect to any data source imaginable.

## How do plugins work

Plugins are implemented as python scripts which have a few methods that they must implement. Beyond that, there are really no rules. Plugins can do just about anything under the sun as long as they return usible data in the following format

### Data Format

Contrary to what you may guess at first, Data Loader Plugins __Do Not__ return data in the squirro item format, but produce flat JSON objects. The data that is produced by your data loader plugin should look like this:
```json
{
    "document_title": "...",
    "author": "...",
    "section": "...",
    "pub_date": "...",
    "content": "...",
    "tags": "...",
}
```
It is also important to note that if one of these fields has multiple values, they should all be concatenated together in a string. Passing multiple values in the form of a list is not supported.
```python
    # Yes
    "tags": "tech|software|AI",

    # No
    "tags": ["tech", "software", "AI"],
```
The transition from flat JSON data into the squirro item format is done automatically by the data loader as shown below:

![alt text](https://docs.google.com/drawings/d/1QZnJN9j4B_MG8X98DLnkXagVF53S10EMiR34wcBH-wQ/pub?w=1258&amp;h=598 "Data Flow Diagram")

### The DataSource Class

To make a data loader plugin, your python script should create an instance of the DataSource class that implements at least the following methods:
* `connect` - Steps required to connect to a data source before data can be extracted from it. _Can be left blank if not required_
* `disconnect` - Steps required to disconnect from a data source after data has been extracted from it. _Can be left blank if not required_
* `getDataBatch` - The method (implemented as a generator) which is called to get batches of data from the plugin
* `getSchema` - A method which returns a list of all the fields within each of the items returned by the plugin. This tells the Data Loader which fields are available for mapping with `--map-id`, `--map-title`, `--map-body`, etc.
* `getJobId` - This method should return a unique ID based on the parameters of the data loading job. This will often be a hash of any other parameters used.
* `getArguments` - This method returns a list of dictionaries. Each dictionary specifies the details for a custom arugment which can be added by the plugin. These additional arguments allow you to pass additional information to the plugin as needed.

## Example Walkthrough
```python
"""
Dataloader Plugin Example - Fake post data
"""
import hashlib
import logging
import requests

from squirro.dataloader.data_source import DataSource

log = logging.getLogger(__name__)


class ExampleSource(DataSource):
    """
    An Example data loader Plugin
    """

    def __init__(self):
        pass

    def connect(self, inc_column=None, max_inc_value=None):
        """Connect to the source"""
        # Nothing to do
        pass

    def disconnect(self):
        """Disconnect from the source."""
        # Nothing to do
        pass

    def getDataBatch(self, batch_size):
        """
        Generator - Get data from source on batches.

        :returns a list of dictionaries
        """

        rows = []

        for row in self.get_example_posts():
            # Emit a `row` here that's flat dictionary. If that's not the case
            # yet, transform it here.
            # But do not return a Squirro item - that's the job of the data
            # loader configuration (facets and mapping).
            rows.append(row)
            if len(rows) >= batch_size:
                yield rows
                rows = []

        if rows:
            yield rows

    def get_example_posts(self):
        """Get some fake example posts from an API endpoint"""

        number_of_posts = self.args.number_of_posts

        for post_number in range(1, number_of_posts + 1):

            post_url = 'http://jsonplaceholder.typicode.com/'\
                      'posts/{number}'.format(
                            number=post_number)

            response = requests.get(post_url)
            post_content = response.json()

            yield post_content

    def getSchema(self):
        """
        Return the schema of the dataset
        :returns a List containing the names of the columns retrieved from the
        source
        """

        schema = [
            'userId',
            'id',
            'title',
            'body'
        ]

        return schema

    def getJobId(self):
        """
        Return a unique string for each different select
        :returns a string
        """
        # Generate a stable id that changes with the main parameters
        m = hashlib.sha256()
        m.update(unicode(self.args.number_of_posts))
        job_id = m.hexdigest()
        log.debug("Job ID: %s", job_id)
        return job_id

    def getArguments(self):
        """
        Get arguments required by the plugin
        """

        return [
            {
                "name": "number_of_posts",
                "help": "number of fake posts to load, max of 100",
                "required": False,
                "default": 100,
                "type": "int",
            }
        ]

```



