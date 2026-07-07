#!/usr/bin/env bash

DIR=$1

cd $DIR
for file in *.geojson; do
    zip "${file}.zip" "$file"
done
cd ..
