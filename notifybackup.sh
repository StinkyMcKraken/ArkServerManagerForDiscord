#!/bin/bash

#lead time before shutting down the server in minutes
time=10

rcon="/home/ark/mcrcon -H 10.0.0.87 -P 27023 -p Swingline5 -s"
message="Broadcast Server Shutdown for BACKUP in"

#run notifications every minute until less than a minute
while (( $time > 1 ))
do
	$rcon "$message $time minutes"
	sleep 1m
	time=$(( $time - 1 ))
done

#send message to server chat with additional information
$rcon "serverchat Server will perform a backup, takes about 20 minutes. Server will be available 5 minutes after TEST ALERT is sent to Discord"

#notifications every 10 seconds in the last minute
time=60
while (( $time > 10 ))
do
	$rcon "$message $time seconds"
	sleep 10
	time=$(( $time - 10 ))
done

#notifications every second in the last 10 seconds
while (( $time > 0 ))
do
	$rcon "$message $time seconds"
	sleep 1
	time=$(( $time - 1 ))
done

#final notification
$rcon "Broadcast Buh Bye!!  See you in 20 minutes!!"

