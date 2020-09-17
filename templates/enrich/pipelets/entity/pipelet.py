"""
This is a Pipelet Template
"""

from squirro.sdk import PipeletV1, require


@require('log')
class TemplatePipelet(PipeletV1):

    def __init__(self, config):

        self.config = config

    def consume(self, item):
        '''Main method run by the pipelet
        '''

        item.setdefault('entities', {})
        self._enrich(item)

        return item

    def _enrich(self, item):
        '''Code to enrich the item goes here
        '''

        # Create a new entity of type `interest`
        new_entity = {
            "type": "interest",
            "name": "Key priorities is to divest assets",
            "confidence": 0.9,
            "relevance": 0.9,
            "extracts": [{
                "text": "On the contrary, one of the key priorities this year"
                "is to continue divesting assets, is to make sure that we"
                "generate free cash flow reaching the target we gave you",
                "field": "body",
                "confidence": 1,
                "offset": 10,
                "length": 10,
            }],
            "properties": {
                "investor": "Investor Name",
                "deal_type": "Diversification",
                "region": "Europe",
                "industry": "Energy"
            }
        }
        item['entities'] = [new_entity]
