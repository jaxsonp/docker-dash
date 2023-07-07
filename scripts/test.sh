#!/bin/bash

# generate key
keypath="/home/$USER/.ssh/id_srccontainerapi"
rm -f "$keypath" &> /dev/null
rm -f "$keypath.pub" &> /dev/null
ssh-keygen -b 2048 -f "$keypath" -N "" &> /dev/null

# get authorization
username="node2"
ipaddr="10.0.2.6"
password="password"
./src-container-api/scripts/ssh_authorize "$username@$ipaddr" "$keypath.pub" "$password" 