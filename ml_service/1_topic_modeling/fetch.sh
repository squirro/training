#!/bin/bash

set -e

DATADIR=$(dirname "$0")
DATASET=20news-18828

wget https://s3.eu-central-1.amazonaws.com/squirro-datasets/walkthroughs/$DATASET/data.tar.gz
tar -xzvf $DATADIR/data.tar.gz -C $DATADIR
