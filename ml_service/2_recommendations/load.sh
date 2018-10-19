#!/bin/bash

CLUSTER=$1
TOKEN=$2
PROJECT_ID=$3

DATADIR=$(dirname "$0")

squirro_data_load \
    --cluster $CLUSTER \
    --project-id $PROJECT_ID \
    --token $TOKEN \
    --source-script $DATADIR/transcript_plugin.py \
    --manifest-file $DATADIR/transcript_manifest.txt \
    --source-name 'Transcript Corpus' \
    --batch-size 1000 \
    --source-batch-size 1000 \
    --map-body 'body' \
    --map-id 'id' \
    --map-url 'link' \
    --map-created-at 'created_at' \
    --map-title 'title' \
    --facets-file $DATADIR/facets.json \
    --pipelets-file $DATADIR/pipelet_config.json
