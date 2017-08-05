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
