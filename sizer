#!/usr/bin/env bash
URL=$1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SLUG=`echo $URL | sed 's-[:/]-_-g'`
mkdir -p /tmp/$SLUG
cd /tmp/$SLUG

for s in 360 480 640 760 920 1260
do
    $DIR/getImageDimensions.js $URL $s | grep -v "\.svg" |
        awk '{system("'$DIR'/getResizeBenefits.sh \""$1"\" "$2" "$3" "'$s'" "'$s')}' | 
        tee /tmp/$SLUG/results_$s.txt  |
        awk '{optimize_sum += $3;resize_sum+=$5}END{print "Viewport: "'$s',optimize_sum, resize_sum}'
done
