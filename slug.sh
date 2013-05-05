#!/usr/bin/env bash

slug(){
    echo $1 | sed 's/[^[:alnum:]]/_/g'
}


