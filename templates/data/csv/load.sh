#!/usr/bin/env bash
cd $(dirname $0)
set -e
source ../../common/config/config.sh

squirro_data_load -v \
    --token $TOKEN \
    --cluster $CLUSTER \
    --project-id $PROJECT_ID \
    --source-type csv \
    --source-file 'Data.csv' \
    --source-name 'Data' \
    --map-title 'title' \
    --map-abstract 'abstract' \
    --map-body 'body' \
    --map-body-mime 'body_mime' \
    --map-id 'id' \
    --map-url 'link' \
    --map-created-at 'created_at' \
    --facets-file 'facets.json' \
    --title-template-file 'title_template.j2' \
    --body-template-file 'body_template.j2' \
    --pipelets-file 'pipelets.json'
