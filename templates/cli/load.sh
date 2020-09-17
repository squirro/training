#!/usr/bin/env bash
cd $(dirname $0)
set -e
source ../../config/config.sh

log_timestamp=$(date +"%Y_%m_%d")

python main.py -v \
    --cluster $CLUSTER \
    --project-id $PROJECT_ID \
    --token $TOKEN 2>&1 | tee -a "log/cli_${log_timestamp}.log"

#clean old logs
find log/ -type f -mtime +14 -iname \*.log -exec rm -f {} \;
