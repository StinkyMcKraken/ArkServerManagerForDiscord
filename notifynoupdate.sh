#!/bin/bash

#script to send broadcast to server indicating no update is happening
#if an update is in progress, the server will already be in the process
#of starting up and noone will see the message anyway

rcon="/home/ark/mcrcon -H 10.0.0.87 -P 27023 -p Swingline5 -s"
message="Broadcast No Server Update At This Time.  You may resume your game at your convenience"

$rcon "$message"
