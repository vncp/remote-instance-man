#!/bin/bash

while read -r line;
do

  systemctl restart vnc-$line;

done < netids.txt
