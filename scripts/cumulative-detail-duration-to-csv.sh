#!/usr/bin/env bash

# An input file of generated json files from a60-recache.exe, a duration.
# Output is csv with durationn, btiha, upeers, useeds
CDFILE=$1
DUR=$2

if [ ! -n "$CDFILE" ]; then
    echo "Data file input argument not supplied, exiting";
    exit 1;
fi
if [ ! -n "$DUR" ]; then
    echo "Duration (week, day, hour) not supplied, exiting";
    exit 1;
fi


echo "using cumulative-detail data: $CDFILE with duration (${DUR})"

MAXPEERS=`jq '.["collection-all-btiha-total"]|.["upeers-total"]' ${CDFILE}`
MAXBTIHA=`jq '.["collection-all-btiha-total"]|.["btiha-size"]' ${CDFILE}`

# Duration specifics
# week number, btiha size, upeers, useeds
# day number, btiha size, upeers, useeds
filebase="${CDFILE##*/}"
FILE="${filebase%.*}"
OUTPUTFILE="$FILE-by-${DUR}.csv"

echo "outputfile: $OUTPUTFILE"
echo "0,0,0,0" >> $OUTPUTFILE;

# Find durations, like:
# "collection-unique-btiha-day-00133"
# "collection-unique-btiha-week-00016"
DURLIST=${DUR}-values.txt
UDUR="collection-unique-btiha-${DUR}"
grep $UDUR ${CDFILE} | tr -d \{ | tr -d \: | tr -d \" | tr -d ' ' >& $DURLIST


mangle_duration_n_field() {
    FIELD="$1"
    SUBFIELD="$2"

    weeknjq='.["';
    weeknjq+=${FIELD};
    weeknjq+='"]|.["';
    weeknjq+="${SUBFIELD}";
    weeknjq+='"]';

    # Output to temp file.
    echo "$weeknjq" > tmp-${FIELD}-${SUBFIELD}
}


for f in `cat ${DURLIST}`
do
  echo "iteration: $f"
  ITER=`echo $f | sed 's/collection-unique-btiha-//g' | sed 's/.*-//'`
  echo $ITER

  mangle_duration_n_field "$f" "btiha-size"
  weeknbtihav=`jq -rf tmp-${f}-btiha-size ${CDFILE}`;

  mangle_duration_n_field "$f" "upeers-total"
  weeknpv=`jq -rf tmp-${f}-upeers-total ${CDFILE}`;

  mangle_duration_n_field "$f" "useeds-total"
  weeknsv=`jq -rf tmp-${f}-useeds-total ${CDFILE}`;

  echo "$ITER,$weeknbtihav,$weeknpv,$weeknsv" >> $OUTPUTFILE;
done


rm tmp-*
rm $DURLIST
echo "" >> $OUTPUTFILE;
