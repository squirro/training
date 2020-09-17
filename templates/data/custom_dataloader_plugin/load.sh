#!/usr/bin/env bash
cd $(dirname $0)
set -e
source ../../common/config/config.sh

squirro_data_load -v \
    --token $TOKEN \
    --cluster $CLUSTER \
    --project-id $PROJECT_ID \
    --log-file 'Data_Loading.log' \
    --source-script 'plugin.py' \
    --first-custom-param $CUSTOM_PARAM_1 \
    --second-custom-param $CUSTOM_PARAM_2 \
    --source-name 'Data' \
    --map-title 'title' \
    --map-abstract 'abstract' \
    --map-body 'body' \
    --map-body-mime 'body_mime' \
    --map-id 'id' \
    --map-url 'link' \
    --map-created-at 'created_at' \
    --facets-file 'facets.json' \
    --pipelets-file 'pipelets.json'
