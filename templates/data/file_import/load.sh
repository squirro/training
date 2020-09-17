#!/usr/bin/env bash
cd $(dirname $0)
set -e
source ../../common/config/config.sh

squirro_file_importer -v \
    --token $TOKEN \
    --cluster $CLUSTER \
    --project-id $PROJECT_ID \
    --source-name 'Documents' \
    contents
