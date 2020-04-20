#!/usr/bin/env bash

# Inputs are per-country-per-resolution slices.

# directory of generated json files from a60-recache.exe
IDIR=$1

# week, day
DURATION=$2

if [ ! -n "$IDIR" ] || [ ! -n "$DURATION" ]; then
    echo "Directory or Duration argument not supplied, exiting";
    exit 1;
fi


cd $IDIR

mkdir slice;
mkdir logs;
mv *.log ./logs;
mv *.json ./slice;

csvfile=${DURATION}s.csv
regions=( ca fl il ny wa )
for i in "${regions[@]}"
do
    echo $i;
    mkdir slice.$i;
    mv slice/*-slice-${i}-*-${DURATION}-*.json ./slice.${i};
    $src/alpha60/scripts/convert-swarm-json-5-to-csv.sh ./slice.$i ${DURATION};
    mv $csvfile slice-$i-${DURATION}s.csv;
done

gplotsrc="${src}/alpha60-results/scripts/swarm-multi-plot-${DURATION}s-plus.gnu"
gnuplot $gplotsrc
