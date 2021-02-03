#!/bin/bash

# send messages to ark server notifying players of impending update
# expecting command line argument providing the name of
# the server to operate on
selfname="${1}"

# go get our variables
source "/home/ark/scripts/globals.sh"

# lead time before shutting down the server in minutes
# figure out how to test for time variable.  if unset, then give it a default
# default time specified in globals.sh

message="Broadcast Server will Shutdown for update in"

# run notifications every minute until less than a minute
while (( ${time} > 1 ))
do
	tempmessage="${message} ${time} minutes"
  echo ${tempmessage}
  ${rcon} ${tempmessage}
	sleep 1m
	time=$(( ${time} - 1 ))
done

# send message to server chat with additional information
tempmessage="serverchat Server will shutdown to perform updates. Server will be available in about 10 minutes"
echo ${tempmessage}
${rcon} ${tempmessage}

# notifications every 10 seconds in the last minute
time=60
while (( ${time} > 10 ))
do
	tempmessage="${message} ${time} seconds"
  echo ${tempmessage}
  ${rcon} ${tempmessage}
	sleep 10
	time=$(( ${time} - 10 ))
done

# notifications every second in the last 10 seconds
while (( ${time} > 0 ))
do
	tempmessage="${message} ${time} seconds"
  echo ${tempmessage}
  ${rcon} ${tempmessage}
	sleep 1
	time=$(( ${time} - 1 ))
done

# final notification
tempmessage="Broadcast Bansai!!"
echo ${tempmessage}
${rcon} ${tempmessage}
