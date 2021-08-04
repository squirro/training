"""Load data from the Squirro Fake News Training API"""


import hashlib
import json
import logging
import urllib.parse

import requests
from squirro.dataloader.data_source import DataSource

log = logging.getLogger(__name__)


class FakeNewsDataSource(DataSource):
    """FakeNews Plugin for the sq_data_loader.

    Features:
    * Load a single section of the news
    * Full and Incremental load
    * Web UI and CLI Support
    """

    def __init__(self):
        pass

    def connect(self, inc_column=None, max_inc_value=None):
        if self.args.reset:
            log.info("Resetting key-value stores")
            self.key_value_cache.clear()
            self.key_value_store.clear()

        # create a requests session object so we get connection pooling
        self.requests = requests.Session()

    def disconnect(self):
        # close the https sesssion
        self.requests.close()

    def getDataBatch(self, batch_size=100):

        items = []

        # iterate all requests sections
        for section in self.args.section:
            # continue from last run or if not present start from 0
            since = self.key_value_store.get(section, 0)
            log.info(f'Loading section "{section}" since ID {since}')

            while True:
                log.info(f" - fetching {self.args.source_batch_size} since ID {since}")
                data_batch = self.getNewsBatch(
                    section=section, count=self.args.source_batch_size, since=since
                )

                articles = data_batch.get("news")

                if not articles:
                    log.info(
                        f"- no new articles found, end of section {section} reached."
                    )
                    break

                for article in articles:

                    item = {}
                    # get any of the fields in the schema
                    # the main task is to flatten the data into a flat dictionary matching the schema
                    # technically this is not needed here as the api response is already flat
                    # but still doing it do demonstrate the idea

                    for key, value in article.items():
                        item[key] = value

                    log.info(f'  - {item["id"]}: {item["headline"]}')

                    items.append(item)

                    if len(items) == batch_size:
                        # we collected a full batch and hand it over to the data loader
                        yield items
                        items = []

                # forward one page in the api
                since = data_batch["next"]

                # store the since value, so we can resume later
                self.key_value_store[section] = since

                # is there more data
                if data_batch["eof"]:
                    log.info(f" - end of section {section} reached.")
                    break

        if items:
            yield items

        return

    def getSchema(self):

        # get a sample response from the api to read out all available fields
        # for such a simple api we could also hard code the schema

        data_batch = self.getNewsBatch(section="sport", count=1, since=0)
        return data_batch["news"][0].keys()

    def getJobId(self) -> str:
        """Generate a stable ID that changes with the main parameters."""
        m = hashlib.blake2b(digest_size=20)
        for v in (self.args.endpoint, self.args.section):
            m.update(repr(v).encode())

        job_id = m.hexdigest()
        log.info("Job ID: %r", job_id)
        return job_id

    def getArguments(self):
        return [
            {
                "name": "section",
                "display_label": "Section",
                "help": "Which sections to index",
                "nargs": "*",
                "type": "str",
                "required": True,
                "advanced": False,
            },
            {
                "name": "endpoint",
                "display_label": "API Endpoint",
                "default": "https://fakenews.squirro.com",
                "help": "API Endpoint",
                "type": "str",
                "advanced": True,
            },
        ]

    def getNewsBatch(self, section, count=100, since=0):
        """
        Helper function to get a single batch of news articles from the API
        Implements caching to avoid duplicate roundtrips.
        """

        base_url = f"{self.args.endpoint}/news/{section}"
        request_params = {"count": count, "since": since}
        url = base_url + "?" + urllib.parse.urlencode(request_params)

        cache_hit = self.key_value_cache.get(url)

        if cache_hit:
            return json.loads(cache_hit)

        # call the api
        response = self.requests.get(url, headers={"Content-Type": "application/json"})

        # throw an exception if the http status is not ok
        response.raise_for_status()

        # parse the json data into a python dict
        data_batch = response.json()

        # log.info(json.dumps(data_batch, indent=2))

        # we only store into cache if this is not the last page
        if not data_batch["eof"]:
            self.key_value_cache[url] = response.text

        return data_batch
