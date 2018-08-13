"""
Pipelet to find forward-looking deals and create entities for them
"""

import json
import nltk
from bs4 import BeautifulSoup
from squirro.sdk import PipeletV1, require
from squirro_client import SquirroClient


@require('log')
class ForwardInterestDealsPipelet(PipeletV1):

    def __init__(self, config):
        with open('pipelet_config.json', 'rb') as f:
            self.config = json.load(f)['ForwardInterestDealsPipelet']['config']
        self.client = self._get_client()

        self.models_project_id = self.config.get('models_project_id')
        self.forward_interest_workflow = self.config.get(
            "forward_interest_workflow_id")
        self.forward_interest_threshold = self.config.get(
            "forward_interest_threshold")
        self.deal_type_workflow = self.config.get("deal_type_workflow_id")
        self.deal_type_threshold = self.config.get("deal_type_threshold")
        self.industry_workflow = self.config.get("industry_workflow_id")
        self.industry_threshold = self.config.get("industry_threshold")

        nltk.download('punkt')

    def consume(self, item):
        '''Main method run by the pipelet on the commandline dataloader.
        '''
        return self._enrich(item)

    def _enrich(self, item):
        '''Code to enrich the item goes here
        '''
        # Tokenize item into sentence items
        sentence_items = self.get_sentence_items(item)

        # Check the sentences for forward interest
        forward_interest_predictions = self.get_predictions(
            self.forward_interest_workflow, sentence_items)

        # Pick out forward interest sentences with super threshold confidence
        forward_interest_sentence_items = []
        for sentence_item in sentence_items:
            prediction = forward_interest_predictions[sentence_item['id']]
            if prediction.get('pos', 0) < self.forward_interest_threshold:
                continue
            forward_interest_sentence_items.append(sentence_item)

        # Check for relevant deal types
        deal_type_predictions = self.get_predictions(
            self.deal_type_workflow, forward_interest_sentence_items)

        # Check for relevant industries
        industry_predictions = self.get_predictions(
            self.industry_workflow, forward_interest_sentence_items)

        for sentence_item in forward_interest_sentence_items:
            properties = {}

            # Get max deal type prediction
            self.add_property(
                properties, 'catalyst',
                deal_type_predictions[sentence_item['id']],
                self.deal_type_threshold)

            # Get max industry prediction
            self.add_property(
                properties, 'industry',
                industry_predictions[sentence_item['id']],
                self.industry_threshold)

            # Early exit if no deal type or industry is strongly matched
            if not properties:
                continue

            self.add_entity(item, properties, sentence_item)

        return item

    def add_property(self, properties, property, prediction, threshold):
        '''Add a predicted property to a properties dictionary if a threshold
        is reached
        '''
        max_class, max_prob = None, 0
        for k, v in prediction.iteritems():
            if v > max_prob:
                max_class, max_prob = k, v
        if max_prob > threshold:
            properties[property] = max_class

    def add_entity(self, item, properties, sentence_item):
        '''Add Entities for any identified catalyst events
        '''
        # Create entity
        text = sentence_item['text']
        offset = item.get('body', '').find(text)
        if offset < 0:
            offset = None
            self.log.warn('Could not find text: %r', text)
        new_entity = {
            "type": "interest",
            "name": "Interest Entity",
            "confidence": 1,
            "relevance": 1,
            "extracts": [{
                "text": text,
                "field": "body",
                "confidence": 1,
                "offset": offset,
                "length": len(text),
            }],
            "properties": properties
        }

        # Add investor
        investor_name = item['keywords'].get('company_ticker', [None])[0]
        if investor_name:
            new_entity['properties']['investor'] = investor_name
        #TODO Use KEE To extract Region names from the sentence

        # Add entity
        item['entities'] = item.get('entities', []) + [new_entity]

    def get_sentence_items(self, item):
        '''Split a text body into a list of sentences and return
        '''
        sentence_items = []
        for paragraph in BeautifulSoup(
                item.get('body', ''), 'lxml').find_all('p'):
            paragraph_text = paragraph.get_text()
            if 'Copyright policy:' in paragraph_text:
                continue
            if 'seekingalpha.com' in paragraph_text:
                continue
            for sentence in nltk.tokenize.sent_tokenize(paragraph_text):
                sentence_items.append({
                    "id": str(len(sentence_items)),
                    "text": sentence,
                    "body": sentence
                })
        return sentence_items

    def get_predictions(self, ml_workflow_id, items, label='label_pred'):
        '''Runs the given machine learning workflow on the supplied items and
        returns the predictions
        '''
        result = self.client.run_machinelearning_workflow(
            project_id=self.models_project_id,
            ml_workflow_id=ml_workflow_id,
            data={'items': items})
        return {item['id']: {k: v for p in item['keywords'][label]
                             for k, v in p.iteritems()}
                for item in result['items']}

    def _get_client(self):
        '''Get a client instance to connect to Squirro
        '''
        client = SquirroClient(None, None, cluster=self.config['cluster'])
        client.authenticate(refresh_token=self.config['token'])
        return client
