#!/bin/bash

# multiple update script identifies running instances based on lgsm lockfiles
# initiates 10 minute warning to running instances, stops each instance, runs
# lgsm force update on the generic instance, and restarts each instance.

# check for running instances by checking for lockfiles
lockfiles=($(find "/home/ark/lgsm/lock" -maxdepth 1 -type f -iname "*.lock" ! -name "*laststart.lock" ! -name "lastupdate.lock" ! -name "backup.lock" -printf "%f\n"))

echo **notifying instances**
# strip trailing '.lock' from filename
# and launch notification script for each lockfile/instance found
# notification scripts should run simultaneously on all active instances
for (( i=0; i<=$(( ${#lockfiles[*]} -1 )); i++ ))
do
  lockfiles[$i]=${lockfiles[$i]%%.lock}
  /home/ark/scripts/sendupdatenotice.sh ${lockfiles[$i]} &
  echo ${lockfiles[$i]}
done
# wait for notification scripts to end
wait

# stop all instances
echo **stopping instances**
for instance in ${lockfiles[@]}
do
  /home/ark/${instance} stop
  echo ${instance} stopped
done
#wait for all instances to stop gracefully
wait

# update lgsm on all instances
# this updates LinuxGSM using arkserver, then copies arkserver to the
# other instances
echo **updating lgsm**
/home/ark/scripts/updatelgsm.sh

# force update server binary since the regular update does not always
# pick up minor updates
# not necessary to run binary updates on each instance
echo **updating server**
/home/ark/arkserver force-update

# restart stopped instances
echo **restarting instances**
for instance in ${lockfiles[@]}
do
  /home/ark/${instance} start
  echo ${instance} started
done
# wait for instance start scripts to complete
wait

# indicate we are done
echo **done!!**
