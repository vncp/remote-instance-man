#!/bin/bash

FILE=users_passwd.txt


while read -r line;
do
  netid=`echo ${line} | cut -d"," -f1`
  passwd=`echo ${line} | cut -d"," -f3`
  echo "${netid},$passwd"
  sudo -u ${netid} bash -c "whoami"
  sudo -u ${netid} bash -c "echo ${passwd} | vncpasswd -f > /home/${netid}/.vnc/passwd"
  sudo -u ${netid} bash -c "chmod 600 /home/${netid}/.vnc/passwd"
done < ${FILE}

echo "Done."
