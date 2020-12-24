#!/bin/bash

#expecting command line argument providing the name of
#the server to operate on
selfname="${1}"

#go get our variables
source "/home/ark/scripts/globals.sh"
#lead time before shutting down the server in minutes
# figure out how to test for time variable.  if unset, then give it a default

message="Broadcast Server will Shutdown for update in"

#run notifications every minute until less than a minute
while (( ${time} > 1 ))
do
	${rcon} "${message} ${time} minutes"
	sleep 1m
	time=$(( ${time} - 1 ))
done

${rcon} "serverchat Server will shutdown to perform updates. Server will be available in about 10 minutes"

#notifications every 10 seconds in the last minute
time=60
while (( ${time} > 10 ))
do
	${rcon} "${message} ${time} seconds"
	sleep 10
	time=$(( ${time} - 10 ))
done

#notifications every second in the last 10 seconds
while (( ${time} > 0 ))
do
	${rcon} "${message} ${time} seconds"
	sleep 1
	time=$(( ${time} - 1 ))
done

#final notification
${rcon} "Broadcast Bansai!!"
