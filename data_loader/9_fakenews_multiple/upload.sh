#!/bin/bash
set -e

CLUSTER="https://..."
TOKEN="..."

squirro_asset dataloader_plugin upload -t $TOKEN -c $CLUSTER -f ../9_fakenews_multiple
