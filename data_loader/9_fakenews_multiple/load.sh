#!/bin/bash
set -e
cd "$(dirname "$0")"

CLUSTER="https://..."
TOKEN="..."
PROJECT_ID="..."

squirro_data_load -v \
    --cluster $CLUSTER \
    --token $TOKEN \
    --project-id $PROJECT_ID \
    --source-script 'fakenews_plugin.py' \
    --source-name "Fake News" \
    --source-batch-size 100 \
    --batch-size 100 \
    --endpoint "https://fakenews.squirro.com" \
    --section "sport" "finance" \
    --map-title 'headline' \
    --map-body 'body' \
    --map-id 'id' \
    --map-url 'article_uri' \
    --map-created-at 'date' \
    --facets-file 'facets.json'
