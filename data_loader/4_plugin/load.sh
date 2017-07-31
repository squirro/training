#!/bin/bash
set -e

CLUSTER="http://...squirro.net/"
TOKEN="...abc..."
PROJECT_ID="...123..."

squirro_data_load -v \
    --cluster $CLUSTER \
    --token $TOKEN \
    --project-id $PROJECT_ID \
    --source-script 'post_plugin.py' \
    --number-of-posts 100 \
    --source-name 'Posts' \
    --map-title 'title' \
    --map-body 'body' \
    --map-id 'id' \
    --facets-file 'facets.json'
