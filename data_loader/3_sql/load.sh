#!/bin/bash
set -e

CLUSTER="http://...squirro.net/"
TOKEN="...abc..."
PROJECT_ID="...123..."

squirro_data_load -v \
    --cluster $CLUSTER \
    --token $TOKEN \
    --project-id $PROJECT_ID \
    --source-type database \
    --db-connection 'mysql://root:@localhost/database-name'
    --input-file 'query.sql'
    --source-name 'Database Query' \
    --map-title 'title' \
    --map-body 'body' \
    --map-id 'id' \
    --map-url 'link' \
    --map-created-at 'created_at' \
    --facets-file 'facets.json'
