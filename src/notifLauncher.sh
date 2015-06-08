#!/bin/bash

cd ~/Dokumente/Dev/Python/Happyminday/src 
python HappyMinday.py -m 1 | ./notif.sh
python HappyMinday.py -d 0 | ./notif.sh
#read -n1 -r -p "Press any key to continue..." key
