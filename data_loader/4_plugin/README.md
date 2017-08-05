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

## Example Plugin
Our example plugin will get some fake post data from the web and add each post as a squirro document.
To get this data, we will use a web API that gives us the fake data to work with. The API is very simple, and responds with JSON data for a fake post. For example:
```bash
$ curl http://jsonplaceholder.typicode.com/posts/1
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```
### Example Walkthrough
We start off the file with a docstring that describes what this plugin does.
Next we want to import everything that we need to make the plugin work, as well as the DataSource base class itself.
```python
"""
Dataloader Plugin Example - Fake post data
"""
import hashlib
import logging
import requests
from squirro.dataloader.data_source import DataSource

log = logging.getLogger(__name__)
```
To start our implementation, we create a new instance of a class which inherits from the DataSource base class.
```python
class ExampleSource(DataSource):
    """
    An Example data loader Plugin
    """
```
If necessary, we can implement an initialization step to handle any initial configuration for the plugin.
```python
    def __init__(self):
        pass
```
Next we can implement the `connect` method (if necessary)
```python
    def connect(self, inc_column=None, max_inc_value=None):
        """Connect to the source"""
        # Nothing to do
        pass
```
and similarly the `disconnect` method (if necessary)
```python
    def disconnect(self):
        """Disconnect from the source."""
        # Nothing to do
        pass
```
Next to implement is `getDataBatch`. Often it is easiest to handle the batching here, and tackle the process of actually fetching the data in another function.
```python
    def getDataBatch(self, batch_size):
        """Generator - Get data from source on batches.
        """

        rows = []
        for row in self.get_example_posts():
            rows.append(row)
            if len(rows) >= batch_size:
                yield rows
                rows = []

        if rows:
            yield rows
```
Now we implement the function that talks to the API and gets the fake post data. We start by getting the desired number of posts from the arguments (which we will define later), and launching an iterative process for each post that we want to get
```python
    def get_example_posts(self):
        """Get some fake example posts from an API endpoint"""

        number_of_posts = self.args.number_of_posts

        for post_number in range(1, number_of_posts + 1):
```
To get a post, we assemble a URL to grab that post ID, and submit an HTTP GET requests to that URL. When we get a response, we load the JSON data from the response. The loaded JSON data is a representation of the post, and we can yield it.
```python
            post_url = 'http://jsonplaceholder.typicode.com/'\
                      'posts/{number}'.format(
                            number=post_number)

            response = requests.get(post_url)
            post_content = response.json()

            yield post_content
```
Next to implement is `getSchema`, which tells us which columns are available in the source data. In most cases it is best to get an example document from the data source and check which fields are available.
In cases of extremely simple data sets, this can be hard coded.
```python
    def getSchema(self):
        """Return the schema of the dataset
        """

        schema = ['userId', 'id', 'title', 'body']
        return schema
```
`getJobId` gets a unique job ID for the current data load. In general this is implemented as a hash of all the unique parameters or custom arguments used by the plugin.
```python
    def getJobId(self):
        """Return a unique string for each different select
        """
        # Generate a stable id that changes with the main parameters
        m = hashlib.sha256()
        m.update(unicode(self.args.number_of_posts))
        job_id = m.hexdigest()
        log.debug("Job ID: %s", job_id)
        return job_id
```
The last method to implement is `getArguments`. This tells the data loader which additional arguments are required by the plugin. When configuring an argument, you can use any attribute supported by the argparse library.
A few things to note:
* The type should be passed in as a string, instead of passing the type itself. For example:
  * (Yes) `"type": "int",`
  * (No) `"type": int,`
* The `name` defined for an argument, is the name of the variable that that argument's value will be accessible at within the plugin. The name of the argument used in the load script will `--` followed by the name with `-` characters intead of underscores.
  * In the example below, our argument has a name of `number_of_posts`. When writing the load script, you would pass this value in as `--number-of-posts`. You could then access that value within the pluin by accessing `self.args.number_of_posts`.
```python
    def getArguments(self):
        """Get arguments required by the plugin
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



