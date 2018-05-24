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

```json
  "pipeline": [
```

#### Loader Step

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


