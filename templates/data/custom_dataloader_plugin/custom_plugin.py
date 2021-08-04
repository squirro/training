"""
Dataloader Plugin Template
"""
import hashlib
import logging

from squirro.dataloader.data_source import DataSource

log = logging.getLogger(__name__)


class TemplateSource(DataSource):
    """
    A Custom data loader Plugin
    """

    def __init__(self):
        pass

    def connect(self, inc_column=None, max_inc_value=None):
        log.debug("Entering connect()")
        log.debug("Incremental Column: %r", inc_column)
        log.debug("Incremental Last Value: %r", max_inc_value)

    def disconnect(self):
        """Disconnect from the source."""
        log.debug("Entering disconnect()")
        # Nothing to do
        pass

    def getDataBatch(self, batch_size):
        """
        Generator - Get data from source on batches.

        :returns a list of dictionaries
        """
        log.debug("Entering getDataBatch()")
        log.debug("Batch Size: %r", batch_size)

        rows = []

        # This call should `yield` and not return all items directly
        content = self.get_content_from_somewhere()

        for row in content:
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

    def getSchema(self):
        """
        Return the schema of the dataset
        :returns a List containing the names of the columns retrieved from the
        source
        """
        log.debug("Entering getSchema()")

        schema = [
            "title",
            "body",
            "body_mime",
            "link",
            "created_at",
            "id",
            "abstract",
            "type",
            "section",
        ]

        return schema

    def getJobId(self):
        """
        Return a unique string for each different select
        :returns a string
        """
        log.debug("Entering getJobId()")

        # Generate a stable id that changes with the main parameters
        m = hashlib.blake2b(digest_size=20)
        for v in (self.args.first_custom_param, self.args.second_custom_param):
            m.update(repr(v).encode())

        job_id = m.hexdigest()
        log.info("Job ID: %s", job_id)
        return job_id

    def getArguments(self):
        """
        Get arguments required by the plugin
        """
        log.debug("Entering getArguments()")

        return [
            {
                "name": "first_custom_param",
                "help": "Custom Dataloader Plugin argument 1",
                "required": True,
                "default": "abc",
            },
            {
                "name": "second_custom_param",
                "help": "Custom Dataloader Plugin argument 2",
                "required": True,
                "default": "abc",
            },
        ]

    def get_content_from_somewhere(self):
        """
        Function that would handle the interaction with the third party
        system and retrive batches of documents. This only serves as an example.
        """

        return [
            {
                "title": "Example 1",
                "body": "Body of Example 1",
                "link": "http://example.com/document1.html",
                "created_at": "2021-01-13T09:10:53",
                "id": "document_1",
                "body_mime": "text/html",
                "abstract": "Abstract of Example 1",
                "type": "Article",
                "section": "Finance",
            },
            {
                "title": "Example 2",
                "body": "Body of Example 2",
                "body_mime": "text/html",
                "link": "http://example.com/document2.html",
                "created_at": "2021-01-15T13:20:01",
                "id": "document_2",
                "abstract": "Abstract of Example 2",
                "type": "Article",
                "section": "Sport",
            },
        ]
