#!/bin/bash
set -e

squirro_asset pipelet \
    consume \
    "company_size.py" \
    -i "test_item.json"
