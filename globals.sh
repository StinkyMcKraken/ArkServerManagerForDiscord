#!/bin/bash

#global variables for johnny kay's ark notification scripts
# setup variables used by multiple scripts
configdirserver="/home/ark/lgsm/config-lgsm/arkserver"
serveradminpassword="Swingline5"
mcrconpath="/home/ark/mcrcon"
time=10  # time in minutes for notifications before server shutdown

# retrieve instance info from lgsm config files
if [ -f "${configdirserver}/_default.cfg" ]; then
  source "${configdirserver}/_default.cfg"
fi
if [ -f "${configdirserver}/common.cfg" ]; then
  source "${configdirserver}/common.cfg"
fi
if [ -f "${configdirserver}/${selfname}.cfg" ]; then
  source "${configdirserver}/${selfname}.cfg"
fi

# must have ip address defined in the lgsm config serverfiles
# I haven't done the whole figure out what the ip is automatically yet
if [ "${ip}" == "0.0.0.0" ]||[ "${ip}" == "" ]; then
  echo "Please specify IP in common.cfg or ${selfname}.cfg"
  exit 1
fi

rcon="${mcrconpath} -H ${ip} -P ${rconport} -p ${serveradminpassword} -s"
