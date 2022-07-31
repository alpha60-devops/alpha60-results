#!/usr/bin/env bash

# directory of generated json files from a60-recache.exe
IDIR=$1

# cumulative detail file
CDJSON="*cumulative-detail.json"
CDFILE=`find ${IDIR} -type f -name $CDJSON`
echo "found cumulative-detail data: $CDFILE"

MAXPEERS=`jq '.["collection-all-btiha-total"]|.["upeers-total"]' ${CDFILE}`
MAXBTIHA=`jq '.["collection-all-btiha-total"]|.["btiha-size"]' ${CDFILE}`

# week number, btiha size, upeers, useeds
OUTPUTFILE="cumulative-detail-by-week.csv"
echo "0,0,0,0" >> $OUTPUTFILE;

mangle_week_n_field_4() {
    ITER="$1"
    FIELD="$2"

    weekfieldn="collection-unique-btiha-week-0000${ITER}"
    weeknjq='.["';
    weeknjq+="${weekfieldn}";
    weeknjq+='"]|.["';

    weeknjq+="${FIELD}";
    weeknjq+='"]';

    # Output to temp file.
    echo "$weeknjq" > tmp-${ITER}-${FIELD}
}


for (( c=1; c < 10; c++ ))
do
  echo "iteration: $c"
  mangle_week_n_field_4 "$c" "btiha-size"
  weeknbtihav=`jq -rf tmp-${c}-btiha-size ${CDFILE}`;
  if [ "$weeknbtihav" != "null" ]
  then
      mangle_week_n_field_4 "$c" "upeers-total"
      weeknpv=`jq -rf tmp-${c}-upeers-total ${CDFILE}`;

      mangle_week_n_field_4 "$c" "useeds-total"
      weeknsv=`jq -rf tmp-${c}-useeds-total ${CDFILE}`;

      echo "$c,$weeknbtihav,$weeknpv,$weeknsv" >> $OUTPUTFILE;
  else
      echo "done....";
      break;
  fi
done


mangle_week_n_field_3() {
    ITER="$1"
    FIELD="$2"

    weekfieldn="collection-unique-btiha-week-000${ITER}"
    weeknjq='.["';
    weeknjq+="${weekfieldn}";
    weeknjq+='"]|.["';

    weeknjq+="${FIELD}";
    weeknjq+='"]';

    # Output to temp file.
    echo "$weeknjq" > tmp-${ITER}-${FIELD}
}


for (( c=10; c < 100; c++ ))
do
  mangle_week_n_field_3 "$c" "btiha-size"
  weeknbtihav=`jq -rf tmp-${c}-btiha-size ${CDFILE}`;
  if [ "$weeknbtihav" != "null" ]
  then
      echo "iteration: $c"

      mangle_week_n_field_3 "$c" "upeers-total"
      weeknpv=`jq -rf tmp-${c}-upeers-total ${CDFILE}`;

      mangle_week_n_field_3 "$c" "useeds-total"
      weeknsv=`jq -rf tmp-${c}-useeds-total ${CDFILE}`;

      echo "$c,$weeknbtihav,$weeknpv,$weeknsv" >> $OUTPUTFILE;
  else
      echo "done....";
      break;
  fi
done


rm tmp-*

echo "" >> $OUTPUTFILE;
