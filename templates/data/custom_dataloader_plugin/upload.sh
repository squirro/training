#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source ../../common/config/config.sh

squirro_asset dataloader_plugin upload -t $TOKEN -c $CLUSTER -f ../custom_dataloader_plugin
