#!/usr/bin/env bash

# Inputs are per-country-per-resolution slices.

# directory of generated json files from a60-recache.exe
IDIR=$1

# week, day
DURATION=$2

cd $IDIR

mkdir slice;
mkdir logs;
mv *.log ./logs;
mv *.json ./slice;

mkdir slice.4k slice.1080 slice.720 slice.sd;

mv slice/*-slice-*2160*.json ./slice.4k/;
mv slice/*-slice-*1080*.json ./slice.1080/;
mv slice/*-slice-*720*.json ./slice.720/;
mv slice/*-slice-*sd*.json ./slice.sd/;

draw=${DURATION}s.csv
$src/alpha60/scripts/convert-swarm-json-5-to-csv.sh ./slice.4k ${DURATION};
mv $draw r4k-${DURATION}s.csv;

$src/alpha60/scripts/convert-swarm-json-5-to-csv.sh ./slice.1080 ${DURATION};
mv $draw r1080-${DURATION}s.csv;

$src/alpha60/scripts/convert-swarm-json-5-to-csv.sh ./slice.720 ${DURATION};
mv $draw r720-${DURATION}s.csv;

$src/alpha60/scripts/convert-swarm-json-5-to-csv.sh ./slice.sd ${DURATION};
mv $draw rsd-${DURATION}s.csv;

gnuplot $src/alpha60-results/scripts/swarm-multi-plot-${DURATION}s.gnu
