#!/bin/bash
# Displays argument text (with several lines if necessary)
# in a notification bubble, using notify-send

data=$1
displayed_text=""
while read data; do displayed_text+=$'\n'$data; done;

notify-send "$displayed_text" 
