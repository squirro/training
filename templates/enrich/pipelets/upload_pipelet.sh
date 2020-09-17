#!/usr/bin/env bash
cd $(dirname $0)
set -e
source ../../common/config/config.sh

squirro_asset -vv pipelet upload \
    --token $TOKEN \
    --cluster $CLUSTER \
    'pipelet.py' \
    'Pipelet Name'
