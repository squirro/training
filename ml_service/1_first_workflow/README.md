# A Workflow Example

## What is a workflow
A workflow is a sequence of steps for loading, preparing, processing, and saving data.

## Goal
The goal of this workflow is to be able to predict the gender of a person based on their first name.

We have a set of pre-labeled data that looks like this:
* `Robert` -> `M`
* `Jessica` -> `F`
* `Michael` -> `M`

And using that historical data would like to be able to predict the gender of a new name, even if we haven't seen it before.

* `Prediction(Kelly)` -> `?`

## Annotated Example

### Specifying the Datasets
Separate datasets can be specified for each of the tasks
1. Training the model on labeled data
2. Testing the model on data that it hasn't seen previously
3. Processing data that we want to predict a label for

Here, you can use the standard Squirro query syntax to specify which subsets of the data in your project you want to use for each specific task.

```json
{
  "dataset": {
    "train": {
      "query_string": "-gender:*"
    },
    "test": {
      "query_string": "-gender:*"
    },
    "process": {
      "query_string": "-pred_gender:*"
    },
  },
```

### Analyzer Specification

```json
  "analyzer": {
    "type": "classification",
    "tag_field": "keywords.pred_gender",
    "label_field": "keywords.gender"
  },
```

### Building the Pipeline
The pipeline defines the series of steps that all of the data goes through. This includes both data that is being used to train the model, as well as data that is being processed by the trained model.

```json
  "pipeline": [
```

#### Pipeline Step Format
Every step in the pipeline has a consistent format.
The step has two keys which will always be present:
* `step`: Specifies the broad type of operation that the step performs. Valid options are:
  * `loader`
  * `filter`
  * `normalizers`
  * `tokenizer`
  * `embedder`
  * `checkpoint`
  * `classifier`
  * `clusterer`
  * `saver`
* `type`: Specifies the specific implementation of that type of step to use. For example, a loader step can be either a `squirro_query_loader`, a `json_loader`, or a `csv_loader`.

```json
    {
      "step": "general-type",
      "type": "specific-type",
      // Additional config options for the step
    },
```

#### Loader Step
The loader step is responsible for providing the iems to be consumed by the model.

```json
    {
      "step": "loader",
      "type": "squirro_query",
      "fields": [
        "keywords.gender",
        "keywords.first_name"
      ]
    },
```

#### Filtering
Filtering steps can be used to remove items with invalid or useless data, like missing values.

```json
    {
      "step": "filter",
      "type": "empty",
      "fields": [
        "keywords.first_name",
        "keywords.gender"
      ]
    },
    {
      "step": "filter",
      "type": "join",
      "input_field": "keywords.first_name",
      "output_field": "keywords.first_name"
    },
```

#### Normalization

```json
    {
      "step": "normalizers",
      "types": [
        "html",
        "punctuation",
        "lowercase",
        "character"
      ],
      "fields": [
        "keywords.first_name"
      ]
    },
```

#### Tokenization

```json
    {
      "step": "tokenizer",
      "type": "spaces",
      "fields": [
        "keywords.first_name"
      ]
    },
```

#### Embedding

```json
    {
      "step": "embedder",
      "type": "dictionary",
      "batch_size": 1024,
      "input_field": "keywords.first_name",
      "output_field": "embedded_text"
    },
```

#### Checkpoint

```json
    {
      "step": "checkpoint",
      "type": "disk",
      "do_randomize": true,
      "batch_size": 1
    },
```

#### Classification

```json
    {
      "step": "classifier",
      "type": "seq2one",
      "batch_size": 1024,
      "dict_name": "dictionary",
      "dropout_fraction": 0.5,
      "embedding_dim": 50,
      "explanation_field": "explanantion",
      "input_field": "embedded_text",
      "label_field": "keywords.gender",
      "labels": [
        "M",
        "F"
      ],
      "max_sequence_length": 1000,
      "mini_batch_size": 64,
      "n_epochs": 10,
      "output_field": "keywords.pred_gender"
    },
```

#### Saving

```json
    {
      "step": "saver",
      "type": "squirro_item",
      "batch_size": 1000,
      "fields": [
        "keywords.pred_gender"
      ]
    }
  ]
}

```


