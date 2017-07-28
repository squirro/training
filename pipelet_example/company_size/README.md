# Company Size Pipelet
This is an example pipelet that we can use to classify companies into a given size based on the number of employees that they have.
## Goal
This pipelet is designed to work with the example company data that we load [here](https://github.com/squirro/training/tree/master/dataloader_example/csv)
The data set looks like this:

|id|company|ticker|ipo_date|number_employees|link|
|---|---|---|---|---|---|
|1|Apple|AAPL|1980-12-12T00:00:00|116000|https://finance.yahoo.com/quote/AAPL|
|2|Google|GOOG|2004-08-19T00:00:00|73992|https://finance.yahoo.com/quote/GOOG|
|3|Microsoft|MSFT|1986-03-13T00:00:00|120849|https://finance.yahoo.com/quote/MSFT|
|4|Amazon|AMZN|1997-05-15T00:00:00|341400|https://finance.yahoo.com/quote/AMZN|
|5|Intel|INTC|1978-01-13T00:00:00|106000|https://finance.yahoo.com/quote/INTC|

Our goal with this pipelet is to classify each company as either a small, medium, large, or huge company based on it's number of employees.
Specifically:
* Small = 0 - 50,000
* Medium = 50,000 - 100,000
* Large = 100,000 - 250,000
* Huge = 250,000+

## Walking through the pipelet code

```python
"""
This Pipelet adds a facet with the company
size based on the number of employees
"""

from squirro.sdk import PipeletV1, require

@require('log')
class CompanySizePipelet(PipeletV1):
```

We start off with a short docstring that describes the general goal of this pipelet, and what it should be used for.

Next we import the required base class for pipelets (`PipeletV1`) and `require` to get injected dependencies.
You can also import any other packages that you need to make the pipelet work correctly.

Finally, we create a class for our pipelet which inherits from the PipeletV1 class, and use the require decorator to inject any dependencies.
```python
    def __init__(self, config):

        self.config = config
```
This is typically a good way to implement the constructor for a pipelet. As the config is only available in `__init__()` by default, assigning it to `self.config` will make it available for the rest of the pipelet code to use.
```python
    def consume(self, item):

        number_of_employees = item['keywords']['number_employees'][0]
        number_of_employees = int(number_of_employees)
```

Next we start implementing the `consume()` method of the pipelet, which takes the contents of a squirro item as the input, and returns a processed version of the same squirro item.

The first step for this pipelet is to fetch the number of employees at the company from within the facet data. Because of the standard squirro item format, facet data is:
* Always stored in lists
* The list is always located within `item['keywords'][facet_name]`

Because the number of employees is stored as the only value within the facet named `number_employees`, we can grab the number of employees for a given company and convert it to an integer using the code shown above.

```python
        if number_of_employees > 250000:
            company_size = 'Huge'

        elif number_of_employees > 100000:
            company_size = 'Large'

        elif number_of_employees > 50000:
            company_size = 'Medium'

        else:
            company_size = 'Small'
```

Once we have the number of employees stored as an integer, the next step is to determine the company size based on that value. For this, we compare the number of employees to our known thresholds for different sizes one at a time.

```python
        item['keywords']['company_size'] = [company_size]

        return item

```

Once we have the company size figured out, we can include the company size information in a new facet. In this example, we are putting the value in a facet called `company_size`. It's important to note that we don't assign the value directly as the facet value, but assign it within a list.
