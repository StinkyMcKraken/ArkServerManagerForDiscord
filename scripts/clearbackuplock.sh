#!/bin/bash

# Sometimes LGSM's backup fails for some reason and leaves backup.lock in
# the lock folder preventing future backups from running.  This script
# deletes the backup.lock file.  Add this script to crontab @reboot to clear
# the lockfile since we know we are not doing a backup at boot

rm /ark/home/lgsm/lock/backup.lock
