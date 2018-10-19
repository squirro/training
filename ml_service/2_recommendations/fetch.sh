#!/bin/bash

set -e

DATADIR=$(dirname "$0")
DATASET=seeking_alpha

wget https://s3.eu-central-1.amazonaws.com/squirro-datasets/walkthroughs/$DATASET/data.tar.gz
tar -xzvf $DATADIR/data.tar.gz -C $DATADIR

wget https://s3.eu-central-1.amazonaws.com/squirro-datasets/walkthroughs/$DATASET/models.tar.gz
tar -xzvf $DATADIR/models.tar.gz -C $DATADIR
