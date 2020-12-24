#!/bin/bash

#send countdown timer for update
/home/ark/scripts/notifyupdate.sh
#do the update thing
/home/ark/aberration update
#send notification of no updates
/home/ark/scripts/notifynoupdate.sh
