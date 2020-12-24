#!/bin/bash

#check for running instances by checking for lockfiles
lockfiles=($(find "/home/ark/lgsm/lock" -maxdepth 1 -type f \( -iname "*.lock" ! -name "*laststart.lock" ! -name "lastupdate.lock" ! -name "backup.lock" \) -printf "%f\n"))

#strip trailing '.lock' from filename
#and launch notification script for each lockfile/server found
#notification scripts should run simultaneously on all active servers
for (( i=0; i<=$(( ${#lockfiles[*]} -1 )); i++ ))
do
  lockfiles[$i]=${lockfiles[$i]%%.lock}
  /home/ark/scripts/sendupdatenotice.sh ${lockfiles[$i]} &
  echo ${lockfiles[$i]}
done
#wait for notification scripts to end
wait

#stop all servers
echo [stopping servers]
for server in ${lockfiles[@]}
do
  /home/ark/${server} stop &
done
#wait for all servers to stop gracefully
wait

#update lgsm on all instances
#this update should run sequentially on each instance instead of simultaneously
echo [updating lgsm]
for server in ${lockfiles[@]}
do
  /home/ark/${server} update-lgsm
done

#force update server binary since the regular update does not always
#pick up minor updates
#not necessary to run binary updates on each instance
echo [updating server]
/home/ark/arkserver force-update

#restart stopped servers
echo [restarting server]
for server in ${lockfiles[@]}
do
  /home/ark/${server} start &
done
#wait for server start scripts to complete
wait

#send test notification to discord indicating backup is complete
echo [done]
#/home/ark/${lockfiles[0]} test-alert
