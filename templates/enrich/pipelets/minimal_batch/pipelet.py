"""
This is a Pipelet Template
"""

from squirro.sdk import PipeletV1, require


@require('log')
class TemplatePipelet(PipeletV1):

    def __init__(self, config):
        self.config = config

    def consume_multiple(self, items):
        '''Main method run by the pipelet
        '''

        for item in items:
            item.setdefault('keywords', {})

            # No need to return item, changing the item in place is enough
            self._enrich(item)

    def _enrich(self, item):
        '''Code to enrich the item goes here
        '''

        item['keywords']['facet'] = ['value']
