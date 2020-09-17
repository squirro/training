"""
This is a Pipelet Template for using a server-side
machine learning workflow for text classification tasks
"""

from squirro.sdk import PipeletV1, require
from squirro_client import SquirroClient


@require('log')
class MLTemplatePipelet(PipeletV1):

    def __init__(self, config):

        self.config = config
        self.keyword_type = config.get('keyword_type', 'weighted')

        # Validate Pipelet Config
        if not self.config.get('cluster'):
            raise ValueError('Missing config option "cluster"')
        if not self.config.get('token'):
            raise ValueError('Missing config option "token"')
        if not self.config.get('project_id'):
            raise ValueError('Missing config option "project_id"')
        if not self.config.get('ml_workflow_id'):
            raise ValueError('Missing config option "ml_workflow_id"')
        if self.keyword_type not in ['weighted', 'string']:
            raise ValueError("keyword_type must be either 'weighted' or 'string'")

        self.client = self._get_client()

    def consume_multiple(self, items):
        '''Main method run by the pipelet on the server side mode.
        '''
        # Directly changes the items in Squirro project. No need to return
        items = self._enrich(items)

    def consume(self, item):
        '''Main method run by the pipelet on the commandline dataloader.
        '''
        items = self._enrich([item])

        for item in items:
            yield item

    def _enrich(self, items):
        '''Code to enrich the item goes here
        '''
        returned_items = self.client.run_machinelearning_workflow(
            project_id=self.config['project_id'],
            ml_workflow_id=self.config['ml_workflow_id'],
            data={'items': items})['items']

        # Add new tags to original items from returned items
        for i, item in enumerate(items):
            if returned_items[i].get('keywords'):
                transformed_keywords = self.transform_keywords(returned_items[i]['keywords'])
                item['keywords'].update(transformed_keywords)

        return items

    def transform_keywords(self, returned_keywords):
        """Transform probabilities from the format used by the
        NLP Lib to the format used by weighted keywords in Squirro
        """

        transformed_keywords = {}
        for facet, facet_values in returned_keywords.iteritems():

            # only transform facets that store probabilities
            if all([isinstance(facet_value, dict) for facet_value in facet_values]):

                if self.keyword_type == 'weighted':
                    transformed_keywords[facet] = facet_values

                elif self.keyword_type == 'string':
                    max_class = None
                    max_prob = 0
                    for prediction in facet_values:
                        for prediction_class, prediction_prob in prediction.iteritems():
                            if prediction_prob > max_prob:
                                max_class = prediction_class
                                max_prob = prediction_prob

                    transformed_keywords[facet] = [max_class]

                else:
                    # Should never get here
                    raise ValueError("Invalid keyword_type {keyword_type} "\
                                     "specified.  must be either 'weighted'"\
                                     " or 'string'".format(
                                        keyword_type=self.keyword_type))

            else:
                transformed_keywords[facet] = facet_values

        return transformed_keywords

    def _get_client(self):
        client = SquirroClient(None, None, cluster=self.config['cluster'])
        client.authenticate(refresh_token=self.config['token'])
        return client
