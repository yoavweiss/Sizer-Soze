#!/usr/bin/env bash

# The script's inputs
URL=$1
WIDTH=$2
HEIGHT=$3
VIEWPORT_WIDTH=$4
VIEWPORT_HEIGHT=$5

# imports
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/slug.sh

# Consts
ORIGINAL=`slug "$URL"|cut -c1-127`
RESIZED=$WIDTH"x"$HEIGHT"_"$ORIGINAL

# Get a file's size
size(){
    ls -l $1 | awk '{print $5}'
}

# Fetch the image
if [ ! -f $ORIGINAL ]
then
    curl -sL "$URL" > $ORIGINAL 2> /dev/null
fi

IS_IMAGE=`file "$ORIGINAL" | egrep "JPEG|PNG|GIF" | wc -l`

if (( $IS_IMAGE == 0 ))
then
   exit 1 
fi

# Resize it to its viewed size
convert $ORIGINAL -geometry $((WIDTH))x$((HEIGHT)) $RESIZED

# Losslessly optimize the output
image_optim $RESIZED 2>/dev/null >/dev/null
ORIGINAL_SIZE=`size $ORIGINAL`

# Get the original image dimensions
ORIGINAL_DIM=`identify -format "%w,%h" "$ORIGINAL"|sed 's/,/x/'`

# Losslessly optimize the original image
cp $ORIGINAL optim_$ORIGINAL
image_optim optim_$ORIGINAL 2>/dev/null >/dev/null
OPTIM_ORIGINAL_SIZE=`size optim_$ORIGINAL`
RESIZED_SIZE=`size $RESIZED`

if (( $RESIZED_SIZE > $OPTIM_ORIGINAL_SIZE ))
then
    RESIZED_SIZE=$OPTIM_ORIGINAL_SIZE
fi

if (( $WIDTH == 0 ))
then
    RESIZED_SIZE=0
fi

echo "$ORIGINAL optimize_savings: "$(($ORIGINAL_SIZE - $OPTIM_ORIGINAL_SIZE))" optimize_and_"$ORIGINAL_DIM"=>"$((WIDTH))x$((HEIGHT)) " "$(($ORIGINAL_SIZE - $RESIZED_SIZE))
