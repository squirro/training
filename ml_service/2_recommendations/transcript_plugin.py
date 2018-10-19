"""
Load RSS Feed data off the filesystem
"""

import json
import hashlib
import logging
from random import shuffle

from squirro.dataloader.data_source import DataSource

log = logging.getLogger(__name__)


class RSSJSONSource(DataSource):
    """
    A Custom data loader Plugin for seekingalpha transcripts
    """

    def __init__(self):
        pass

    def connect(self, inc_column=None, max_inc_value=None):
        """Conect to the source"""
        # Nothing to do
        pass

    def disconnect(self):
        """Disconnect from the source."""
        # Nothing to do
        pass

    def get_news(self):

        with open(self.args.manifest_file, 'r') as manifest_file:
            manifest = manifest_file.read().split('\n')

        shuffle(manifest)

        for data_file in manifest:

            data_file = data_file.strip()
            if not data_file:
                continue

            log.info('processing file {}'.format(data_file))

            with open('content/' + data_file, 'r') as data_file_object:
                file_data = json.load(data_file_object)

            for element in file_data:

                # skip presentations for now
                if not element.get('type') == 'Transcript':
                    continue

                article = {}

                link_text = element.get('link', '')
                if not link_text:
                    continue

                article_title = link_text.split('/')[-1]
                article_title = article_title.replace('-', ' ')

                all_companies = element.get('companies', [{}])
                if not all_companies:
                    primary_company = {
                        "ticker": "Unknown",
                        "name": "Unknown"
                    }
                else:
                    primary_company = all_companies[0]

                article['id'] = element.get('link', '')
                article['title'] = article_title
                article['body'] = element.get('transcript')
                article['created_at'] = element.get('timestamp')
                article['link'] = 'https://seekingalpha.com' + element.get('link', 'Unknown')
                article['company_name'] = primary_company.get('name', 'Unknown')
                article['company_ticker'] = primary_company.get('ticker', 'Unknown')
                article['type'] = 'Full Transcript'
                log.info('article title: %s', article_title)

                yield article

    def getDataBatch(self, batch_size):
        """
        Generator - Get data from source on batches.

        :returns a list of dictionaries
        """

        rows = []

        # This call should ideally `yield` and not return all items directly
        content = self.get_news()

        for row in content:
            # Emit a `row` here that's flat dictionary. If that's not the case
            # yet, transform it here.
            # But do not return a Squirro item - that's the job of the data
            # loader configuration (facets and mapping).
            rows.append(row)
            if len(rows) >= 1:
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
            'title',
            'body',
            'created_at',
            'id',
            'link'
        ]

        return schema

    def getJobId(self):
        """
        Return a unique string for each different select
        :returns a string
        """
        # Generate a stable id that changes with the main parameters
        m = hashlib.sha256()
        m.update(self.args.manifest_file)
        job_id = m.hexdigest()
        log.debug("Job ID: %s", job_id)
        return job_id

    def getArguments(self):
        """
        Get arguments required by the plugin
        """

        return [
            {
                "name": "manifest_file",
                "help": "Manifest for all data files",
                "required": True,
                "default": "manifest.txt",
            }
        ]
