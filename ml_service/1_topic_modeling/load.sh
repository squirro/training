#!/bin/bash

# -- Do not run this script directly.
# -- It should be run from the Jupyter Notebook
# -- as part of the Topic Modeling Walkthrough

CLUSTER=$1
TOKEN=$2
PROJECT_ID=$3

DATADIR=$(dirname "$0")

squirro_data_load -v \
    --cluster $CLUSTER \
    --project-id $PROJECT_ID \
    --token $TOKEN \
    --source-script $DATADIR/20_newsgroups_loader.py \
    --encoding latin1 \
    --location ./data \
    --pipeline2 \
    --map-id id \
    --map-body body \
    --map-title title \
    --source-name '20 newsgroups' \
    --facets-file $DATADIR/facets.json \
    --validation-split 0.1
