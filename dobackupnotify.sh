#!/bin/bash

#do in game countdown
/home/ark/scripts/notifybackup.sh
#stop server
/home/ark/aberration stop
#run backup
/home/ark/aberration backup
#force update
/home/ark/aberration force-update
#start server
/home/ark/aberration start
#send test alert to notify when backup is complete
/home/ark/aberration test-alert

