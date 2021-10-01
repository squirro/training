#!/usr/bin/env bash
cd "$(dirname "$0")"
set -e
source ../../common/config/config.sh

squirro_asset dataloader_plugin upload -t $TOKEN -c $CLUSTER -f ../custom_dataloader_plugin
