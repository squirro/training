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
        log.debug("Incremental Column: %r", inc_column)
        log.debug("Incremental Last Value: %r", max_inc_value)

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

        # This call should ideally `yield` and not return all items directly
        content = get_content_from_somewhere()

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

        schema = [
            "title",
            "body",
            "link",
            "created_at",
            "id",
            "summary",
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
