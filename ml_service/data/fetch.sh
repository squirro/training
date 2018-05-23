#!/bin/bash

set -e

DATADIR=$(dirname "$0")
DATASET=20news-18828

aws s3 sync s3://squirro-datasets/$DATASET $DATADIR
tar -xzvf $DATADIR/$DATASET.tar.gz -C $DATADIR
