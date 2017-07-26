"""
This is a Pipelet Template
"""

from squirro.sdk import PipeletV1, require

@require('log')
class TemplatePipelet(PipeletV1):

    def __init__(self, config):

        self.config = config

    def consume(self, item):

        self._enrich(item)
        return item

    def _enrich(self, item):

        # Code to enrich the item goes here
        item.setdefault('keywords', {})
        item['keywords']['facet'] = ['value']
