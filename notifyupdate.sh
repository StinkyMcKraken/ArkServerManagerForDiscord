#!/bin/bash

#lead time before shutting down the server in minutes
time=10

rcon="/home/ark/mcrcon -H 10.0.0.87 -P 27023 -p Swingline5 -s"
message="Broadcast Server **may** Shutdown for update in"

#run notifications every minute until less than a minute
while (( $time > 1 ))
do
	$rcon "$message $time minutes"
	sleep 1m
	time=$(( $time - 1 ))
done

$rcon "serverchat Server *Might* shutdown if there is an update for ARK. A notification will be sent to Discord when the update is complete.  Server will be available roughly 5 minutes after the notification."

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
$rcon "Broadcast Bansai!!"

