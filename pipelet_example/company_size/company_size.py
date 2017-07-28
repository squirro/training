"""
This Pipelet adds a facet with the company
size based on the number of employees
"""

from squirro.sdk import PipeletV1, require

@require('log')
class CompanySizePipelet(PipeletV1):

    def __init__(self, config):

        self.config = config

    def consume(self, item):

        number_of_employees = item['keywords']['number_employees'][0]
        number_of_employees = int(number_of_employees)

        if number_of_employees > 250000:
            company_size = 'Huge'

        elif number_of_employees > 100000:
            company_size = 'Large'

        elif number_of_employees > 50000:
            company_size = 'Medium'

        else:
            company_size = 'Small'

        item['keywords']['company_size'] = [company_size]

        return item
