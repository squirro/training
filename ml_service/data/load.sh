#!/bin/bash

CLUSTER=https://centos7.squirro.net/
PROJECT_ID=OdzZ_GYiSn2UpixkvA7kwA
TOKEN=f91a5983aaaa25598ab6ce7351e271c5f083d405cb1a9f98289987a54ad0659535cbb5c6fb7c1b6e427101213f0d46b8024743653b1aab5f59e4f5da2bb82fea

DATADIR=$(dirname "$0")

squirro_data_load -v \
    --cluster $CLUSTER \
    --project-id $PROJECT_ID \
    --token $TOKEN \
    --source-script $DATADIR/20_newsgroups_loader.py \
    --encoding latin1 \
    --location . \
    --pipeline2 \
    --map-id id \
    --map-body body \
    --map-title title \
    --source-name '20 newsgroups' \
    --facets-file $DATADIR/facets.json \
    --validation-split 0.1
