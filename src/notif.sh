#!/bin/bash
# Displays argument text (with several lines if necessary)
# in a notification bubble, using notify-send

data=$1
#second argument can be an additional message
displayed_text=$2
while read data; do displayed_text+=$data$'\n'; done;

if [ "$displayed_text" ]
then notify-send "$displayed_text" 
fi
