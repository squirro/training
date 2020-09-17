"""
This is a Pipelet Template
"""

from squirro.sdk import PipeletV1, require


VERSION = '1.0.0'
VERSION_FACET = 'pipelet_version'


@require('log')
class TemplatePipelet(PipeletV1):

    def __init__(self, config):

        self.config = config

        self.version = config.get('version', VERSION)
        self.version_facet = config.get('version_facet', VERSION_FACET)

        if not isinstance(self.version, basestring) \
                and self.version is not False:
            raise ValueError('Version must be specified as a string '
                             'or set to false')

        if not isinstance(self.version_facet, basestring):
            raise ValueError('Version facet must be specified as a string')

    def consume(self, item):
        '''Main method run by the pipelet
        '''

        item.setdefault('keywords', {})

        self._enrich(item)

        if self.version is not False:
            item['keywords'][self.version_facet] = [self.version]

        return item

    def _enrich(self, item):
        '''Code to enrich the item goes here
        '''

        item['keywords']['facet'] = ['value']
