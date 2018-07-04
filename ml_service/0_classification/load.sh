#!/bin/bash

CLUSTER=$1
TOKEN=$2
PROJECT_ID=$3

DATADIR=$(dirname "$0")

squirro_data_load -v \
    --cluster $CLUSTER \
    --project-id $PROJECT_ID \
    --token $TOKEN \
    --pipeline2 \
    --map-body text \
    --facets-file $DATADIR/facets.json \
    --source-file $DATADIR/data.csv \
    --source-name 'forward_interest' \
    --source-type 'csv' \
    --source-profile minimal
