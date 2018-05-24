#!/bin/bash

CLUSTER=...
TOKEN=...
PROJECT_ID=...

squirro_data_load -v \
    --cluster $CLUSTER \
    --token $TOKEN \
    --project-id $PROJECT_ID \
    --source-type csv \
    --source-file 'people.csv' \
    --source-name 'People' \
    --facets-file 'facets.json' \
    --title-template-file 'title_template.j2' \
    --body-template-file 'body_template.j2'
