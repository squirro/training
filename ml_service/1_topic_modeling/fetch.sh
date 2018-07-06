#!/bin/bash

set -e

DATADIR=$(dirname "$0")
DATASET=20news-18828

aws s3 sync s3://squirro-datasets/walkthroughs/$DATASET $DATADIR --profile squirro-internal
tar -xzvf $DATADIR/data.tar.gz -C $DATADIR
