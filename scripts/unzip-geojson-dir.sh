#!/usr/bin/env bash

DIR=$1

cd $DIR
for f in *.zip; do unzip "$f"; done
cd ..
