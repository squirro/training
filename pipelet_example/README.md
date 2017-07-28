# Pipelets

## What is a Pipelet?
Pipelets are plugins to the Squirro pipeline, used to customize how data is processed.
### Where do pipelets fit in the process of loading data?
Pipelets are used to modify data once it has been transformed into the Squirro item format. The Squirro item format is a consistent and predicatble format that all data is changed into before being loaded into Squirro. The step of taking source data (like what is produced by Data Loader plugins) and turning it into the Squirro item format is done automatically by the Squirro Data Loader tool.

![alt text](https://docs.google.com/drawings/d/1QZnJN9j4B_MG8X98DLnkXagVF53S10EMiR34wcBH-wQ/pub?w=1258&amp;h=598 "Data Flow Diagram")

For this reason, you should always design pipelets to work with data that exists in the Squirro item format shown below.
#### The Squirro data format
Once transformed by the data loader, squirro items will always have the same structure.
### What do Pipelets look like?
Pipelets are implemented as Python classes which inherit from the PipeletV1 base class. When you create a pipelet, you only have one method to implement, which is `consume()`
In general, Pipelets will look like this:
```python
"""
This is an Example Pipelet
"""

from squirro.sdk import PipeletV1, require

@require('log')
class ExamplePipelet(PipeletV1):

    def __init__(self, config):

        self.config = config

    def consume(self, item):

        # Enrichment code goes here...
        return item

```
