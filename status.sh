#!/bin/bash

# status script identifies each running server, pulls player list from each
# and outputs the listing

# check for running instances by checking for lockfiles
lockfiles=($(find "/home/ark/lgsm/lock" -maxdepth 1 -type f \( -iname "*.lock" ! -name "*laststart.lock" ! -name "lastupdate.lock" ! -name "backup.lock" \) -printf "%f\n"))

# if no servers running, display message, bugout
if [ -z ${lockfiles[0]} ]
then
  echo "No Servers Running"
  exit 1
fi

# iterate through running server list and pull playerlist from each
for (( i=0; i<=$(( ${#lockfiles[*]} -1 )); i++ ))
do
  # strip trailing '.lock' from filename
  lockfiles[$i]=${lockfiles[$i]%%.lock}
  # output servername
  echo \*\*${lockfiles[$i]}\*\*
  # get variables from lgsm config files
  selfname=${lockfiles[$i]}
  source /home/ark/scripts/globals.sh
  # run rcon command to get player list
  ${rcon} -c listplayers
done
