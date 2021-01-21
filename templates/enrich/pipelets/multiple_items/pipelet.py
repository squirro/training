"""
This is a Pipelet Template for yielding multiple items.

Note this pipelet will only work during the dataloading pipeline.
Using this as a pipeline rerun will not work.
"""
import copy
import hashlib

from squirro.sdk import PipeletV1, require

VERSION = '0.0.1'

@require('log')
class MultipleItemsPipelet(PipeletV1):

    def __init__(self, config):

        self.config = config

    def consume(self, item):
        '''Main method run by the pipelet
        '''

        item.setdefault('keywords', {})

        # Create a new id for the copied item.
        m = hashlib.sha256()
<<<<<<< HEAD
        m.update(item.get('id', '').encode('utf-8'))
        m.update('new_item').encode('utf-8'))
=======
        m.update(unicode(item.get('id', '')))
        m.update(unicode('new_item'))
>>>>>>> 93ca12bb5479129a41bbb70e877c4ed3e5403c67
        new_id = m.hexdigest()

        # This can be expensive, as deepcopy is slow.
        new_item = copy.deepcopy(item)
        new_item['id'] = new_id

        # Enrich the new item
        self.enrich_new_item(new_item)

        # Enrich the original item
        self.enrich_item(item)

        yield item
        yield new_item

    def enrich_new_item(self, item):
        '''Code to enrich the new item goes here
        '''

        item['keywords']['new_item'] = ['copy_Example']

    def enrich_item(self, item):
        '''Code to enrich the original item goes here
        '''

        item['keywords']['original_item'] = ['original_Example']
