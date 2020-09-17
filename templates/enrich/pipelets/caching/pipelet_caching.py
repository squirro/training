"""
This is a template to be used whenever a pipelet accesses
an external resource such as an API where the response
should be cached
"""

import os
import errno
import json
import requests
from hashlib import sha256
from datetime import datetime

from squirro.sdk import PipeletV1, require


API_URL = 'http://api.com'


@require('log')
class TempaltePipelet(PipeletV1):

    def __init__(self, config):

        # If an API key is required
        if 'api_key' not in config:
            raise ValueError('Missing API key')

        self.config = config

    def consume(self, item):
        '''The main method run by the pipelet
        '''

        item.setdefault('keywords', {})
        self._enrich(item)

        return item

    def _enrich(self, item):
        '''Submit some data to a web service and
        enrich the item using the response
        '''

        headers = {
            'key': 'value'
        }

        data = {
            'key2': 'value2'
        }

        response = self.get_response(url=API_URL, headers=headers, data=data)

        # Work with API response
        response_data = response['data']
        response_status_code = int(response['status_code'])

        return item

    '''
    API Response caching framework
    '''

    def get_response(self, url, cache_location='/tmp/response_cache/',
                     store_errors=False, timeout=None, http='GET',
                     headers=None, data=None):
        '''The main method, This is what is called to
        get a remote cached API response
        '''

        # Check the cache first, then if no cache,
        # go to the API to get the folder data
        response_data = self._lookup_cache(
            url, headers, data, cache_location, timeout)

        # Cache Miss
        if not response_data:

            # Make API Request
            response = self.get_web_response(url, http, headers, data)

            if (store_errors) or (int(response['status_code']) < 300):

                try:
                    # Write to cache after successful API response
                    self._write_cache(
                        url, headers, data, response, cache_location)

                except ValueError:

                    # If writing the first time fails, it is useful to try
                    # a second time with the encoding set
                    try:
                        self._write_cache(
                            url, headers, data,
                            response.encode('utf8'), cache_location)

                    except UnicodeEncodeError:
                        print 'Error writing the response to the cache'

        # Cache Hit
        else:
            # work with the res_data as if it were the API response
            response = response_data

        return response

    def get_web_response(self, url, http, headers, data):
        '''Submit an HTTP request to get content
        from a web server
        '''

        if http.upper() == 'GET':
            response = requests.get(url, headers=headers, data=data)

        elif http.upper() == 'POST':
            response = requests.post(url, headers=headers, data=data)

        else:
            raise ValueError('Invalid HTTP Method {method} specified. '
                             'Must use either GET or POST'.format(
                                method=http))

        try:
            response_data = response.json()
        except Exception:
            response_data = response.text

        response_status = response.status_code

        response_dict = {
            "data": response_data,
            "status_code": response_status
        }

        return response_dict

    def _lookup_cache(self, url, headers, data, cache_location, timeout):
        '''Check if a valid cache entry exists for a given request
        '''

        file_path = self._cache_file_name(url, headers, data, cache_location)
        path = os.path.dirname(file_path)
        file_exists = os.path.exists(path)
        if not file_exists:
            return None

        try:
            # Try to get the last modified date of the file
            if (self.get_cache_age(file_path) < timeout) or (not timeout):
                with open(file_path, 'rb') as f:
                    response = json.load(f)['response']
                    return response

            else:
                return None

        except Exception:
            return None

    def get_cache_age(self, file_path):
        '''Figure out how long ago a cache entry was created
        '''

        modified_time = self.get_modified_time(file_path)
        current_time = datetime.now()

        cache_age = current_time - modified_time
        age_days = cache_age.days
        age_seconds = cache_age.seconds
        # Calculate the total number of second elapsed
        total_age_seconds = age_seconds + (86400 * age_days)

        # Convert the total age in seconds into hours (rounded down)
        total_age_hours = total_age_seconds // 3600

        return total_age_hours

    def get_modified_time(self, file_path):
        '''Get the last modified time of a file'''

        time_stamp = os.path.getmtime(file_path)

        return datetime.fromtimestamp(time_stamp)

    def _write_cache(self, url, headers, data, response, cache_location):
        '''Write a cache entry'''

        file_path = self._cache_file_name(url, headers, data, cache_location)
        json_object = {'cache-key': url, 'response': response}

        try:
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path)

        except OSError as ex:
            if ex.errno != errno.EEXIST:
                raise ex

        with open(file_path, 'wb') as f:
            json.dump(json_object, f)

    def _cache_file_name(self, url, headers, data, cache_location):
        '''Generate a cache file name from a request'''

        digest_body = unicode({
            "request": repr(url),
            "headers": headers,
            "data": data
        })

        digest = sha256(digest_body).hexdigest()

        path = os.path.join(
            cache_location, digest[:2], digest[2:4], digest[4:6])

        file_path = path + '/' + digest + '.json'

        return file_path
