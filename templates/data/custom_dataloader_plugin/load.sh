#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source ../../common/config/config.sh

squirro_data_load -v \
    --token $TOKEN \
    --cluster $CLUSTER \
    --project-id $PROJECT_ID \
    --source-script 'custom_plugin.py' \
    --first-custom-param "$(getval first_param squirro)" \
    --second-custom-param "$(getval second_param squirro)" \
    --source-name 'Data' \
    --map-title 'title' \
    --map-abstract 'abstract' \
    --map-body 'body' \
    --map-body-mime 'body_mime' \
    --map-id 'id' \
    --map-url 'link' \
    --map-created-at 'created_at' \
    --facets-file 'facets.json'

    # Optional for pipelets
    #--pipelets-file 'pipelets.json'

    # Optional logging output to a file
    #--log-file 'data_loading.log'
