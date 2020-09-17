"""
This is a Template for a Pipelet that facilitates
access to file data for binary files.
"""

import base64

from squirro.sdk import PipeletV1, require
from squirro.common.config import get_config


@require('log')
class TemplatePipelet(PipeletV1):

    def __init__(self, config):

        self.config = config
        self.storage_config = get_config('squirro.lib.storage')
        try:
            from squirro.lib.storage.handler import StorageHandler
            self.storage = StorageHandler(self.storage_config)
        except ImportError:
            self.log.error('Cannot Import StorageHandler. Assuming'
                           'the pipelet is not running server-side')
            self.storage = None

    def consume(self, item):
        '''Main method run by the pipelet'''

        item.setdefault('keywords', {})

        file_data = self.get_file_content_server_side(item)
        if not file_data:
            file_data = self.get_file_content_client_side(item)

        # Exit if no file data was found
        if not file_data:
            return item

        self._enrich(item, file_data)

        return item

    def _enrich(self, item, file_data):
        '''Code to enrich the item goes here
        In addition to the item, you also have access
        to the file_data
        '''

        pass

    def get_file_content_server_side(self, item):
        '''Try to get file contents as they would exist server side
        '''

        if not self.storage:
            return None

        content_url = item.get('files', [{}])[0].get('content_url', None)

        if not content_url:
            return None

        with self.storage.open(content_url) as f:
            file_data = f.read()

        return file_data

    def get_file_content_client_side(self, item):
        '''Try to get file contents as they would exist client side
        '''

        if not item.get('files'):
            return None

        file_object = item.get('files', [{}])[0]
        file_content = file_object.get('content')

        bin_file_content = base64.b64decode(file_content)

        return bin_file_content
