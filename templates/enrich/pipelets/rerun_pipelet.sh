#!/usr/bin/env bash
cd $(dirname $0)
set -e
source ../../common/config/config.sh

squirro_asset -vv pipelet rerun \
    --token $TOKEN \
    --cluster $CLUSTER \
    --project-id $PROJECT_ID \
    --config '{"key": "value"}' \
    --batch-size 1000 \
    --query '*' \
    'pipelet.py'
