#!/bin/bash

CLUSTER="http://...squirro.net/"
TOKEN="...abc..."

# This command must be run from the parent directory
cd ..

squirro_asset dataloader_plugin \
upload \
--folder '7_upload' \
--token $TOKEN \
--cluster $CLUSTER
